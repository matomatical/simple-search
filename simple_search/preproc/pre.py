import re

from simple_search.preproc.porter2 import stem
from simple_search.preproc.stopwords import STOPWORDS

RE_HTML_TAG = re.compile(r"<[^>]*>")
RE_NON_WORD = re.compile(r"[^\w\d'\-\.]+", flags=re.UNICODE)
def process(document):

    # 1. remove unwanted formatting information:
    document = RE_HTML_TAG.sub(" ", document)

    # 2. segment structure:
    pass # is this necessary for IR?

    # 3. tokenise words:
    # (simple approach, using regex)
    tokens = RE_NON_WORD.split(document)
    
    # 4. normalise words:
    tokens = [normalise(token) for token in tokens]

    # 5. remove unwanted words:
    tokens = [token for token in tokens if token and not stopword(token)]

    return tokens

def stopword(word):

    return word in STOPWORDS

def normalise(word):
    word = word.replace(".", "") # remove internal punct.
    return stem(word)
