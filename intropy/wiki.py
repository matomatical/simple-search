"""Load and parse MediaWiki articles from a Wikipedia dump

For example (after `from intropy import wiki`):

>>> raw_text = wiki.load('Leap year')
>>> raw_text
"A '''leap year''' is a [[year]] in which an extra [[day]] is added to the..."
>>> type(raw_text)
<class 'str'>

>>> wikitext = wiki.parse(raw_text)
>>> wikitext
"A '''leap year''' is a [[year]] in which an extra [[day]] is added to the..."
>>> type(wikitext)
<class 'mwparserfromhell.wikicode.Wikicode'>

>>> wikitext.strip_code()
'A leap year is a year in which an extra day is added to the Gregorian cale...'
>>> wikitext.filter_wikilinks()
['[[year]]', '[[day]]', '[[Gregorian calendar]]', '[[day]]', ...
"""

import os
import bz2

import mwparserfromhell

def setup(datafile, indexfile):
    """Reset global variables to original state with new index and data files

    Call this function if you want to analyse some wikipedia other than the
    Simple English Wikipedia

    - datafile should be the location of the new wikipedia's bz2-compressed
      data file (like data/data.bz2 for the Simple English Wikipedia),
    - indexfile should be the location of the new wikipedia's CONVERTED* index
      file (like data/index.txt for the Simple English Wikipedia)

    *: The index file must be CONVERTED from the format downloaded off the dumps
    website. Please see the LMS for instructions on how to convert the index

    These two parameters are optional. If you exclude them both, you will reset
    the program to be ready to load articles from the Simple English Wikipedia

    NOTE: THIS IS NOT A GOOD EXAMPLE OF PROGRAMMING. DO NOT USE GLOBAL VARIABLES
    """
    global _data_file, _last_stream, _last_stream_offset
    _data_file = open(datafile, 'rb')
    _last_stream = None
    _last_stream_offset = None
    
    global _index_cache, _index_file
    _index_file  = open(indexfile, encoding='utf8')
    _index_cache = {}



def load(name):
    """Load the MediaWiki text for the article called 'name' from the dataset

    Raise an ArticleNotFoundError if this article is not inside the dataset
    """
    global _last_stream, _last_stream_offset, _data_file # see above

    # Using the index, find the location of this article in the data file
    stream_offset, stream_size, pageid = index_lookup(name)
    if stream_offset == None:
        raise ArticleNotFoundError("Missing article: '{}'".format(name))

    # If it happens to be in the same stream as last time, we're in luck!
    # We already decompressed this stream
    if _last_stream_offset == stream_offset and _last_stream is not None:
        stream_decompressed = _last_stream

    # Otherwise, inflate this particular stream from the compressed data
    # file (read the 'stream_size' bytes starting from 'stream_offset')
    else:
        _data_file.seek(stream_offset)
        stream_compressed = _data_file.read(stream_size)
        stream_decompressed = bz2.decompress(stream_compressed).decode('utf8')
        # (and save for next time)
        _last_stream = stream_decompressed
        _last_stream_offset = stream_offset

    # Finally, look inside the decompressed stream for the particular id
    # 'pageid': here's where the text of the article will be!
    try:
        article = stream_decompressed.split('<id>'+pageid+'</id>')[1] \
                                    .split('<text xml:space="preserve">')[1] \
                                    .split('</text>')[0]
        return article

    # And if that didn't work... something is wrong, looks like the pageid must
    # have been missing, or something else wrong with the decompressed XML file
    except IndexError:
        raise ArticleNotFoundError("Internal error: id={}".format(pageid))


def parse(text):
    """Return a wikitext object version of raw MediaWiki-formatted string 'text'

    Just uses mwparserfromhell's 'parse()' function: check out the docs of
    mwparserfromhell for more info
    """
    return mwparserfromhell.parse(text)

class ArticleNotFoundError(Exception):
    """Raise when an attempt to load an article from the dataset fails"""




### INTERNAL FUNCTIONS, NOT INTENDED FOR STUDENT USE (WELCOME TO USE THOUGH) ###

def fold(name):
    """Normalise spacing and casing as per mediawiki conventions
    (space/underscore insensitive, and case insensitive on the
    first letter of the name but not on the rest of the name)

    This function is NOT intended for student use! You probably wont need it.
    """
    spaced_name = name.strip().replace('_', ' ')
    if spaced_name:
        cased_name = spaced_name[0].lower() + spaced_name[1:]
        return cased_name
    else:
        return ''


def index_lookup(query_name):
    """Find an article's position in the data file using the index file or cache

    Return value is a triple (offset, size, pageid), where:

    offset is the offset in bytes of the article's stream in the compressed data
    size is the size in bytes of this compressed stream
    pageid is the (string) id number of the article within the decompressed data

    If the article with that name cannot be found within the index file, return
    (None, None, None)

    This function is 'memoised' to store the contents of the index file as it
    reads the file for the first time

    This function is NOT intended for student use! You probably wont need it.
    """
    global _index_cache, _index_file # see above

    query_name = fold(query_name)

    # first, check to see if we have read the location already? if so, we don't
    # need to consult the index file itself
    if query_name in _index_cache:
        # we found the article in the cache!
        return _index_cache[query_name]
    
    # if we haven't (and there is still stuff left in the index file) we should
    # load more lines and see if we can find this article
    if not _index_file.closed:
        for row in _index_file:
            offset, size, pageid, name = row.strip('\n').split(':', maxsplit=3)
            offset = int(offset)
            size = int(size)
            name = fold(name)

            # cache this lookup for next time
            _index_cache[name] = offset, size, pageid

            if name == query_name:
                # we found the article in the index file!
                return offset, size, pageid
        # if we get to this point, we have finished loading the index into
        # memory: time to close the index file!
        _index_file.close()

    # else, if we get to the end of the index file (this time or maybe some
    # previous time run) and still didn't find this article name, it's not in
    # the index
    return None, None, None
