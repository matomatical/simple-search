"""
Module provides classes and functions for dealing with 

"""

import math
from collections import Counter

class SimpleIndex:
    def __init__(self, documents):
        self._vocabmap = {} # term t -> t's term id
        self._postings = [] # t's term id -> ([d], [f_t,d]) | d <- ds, f_t,d > 0
        self._docfreqs = [] # t's term id -> df_t
        self._docnames = [] # d -> d's name (for lookup in collection)
        self._docnorms = [] # d -> d's normalisation factor (for scaling)
        
        for d, (doc_name, doc_terms) in enumerate(documents):
            self._docnames.append(doc_name)
            self._docnorms.append(1.0 / math.sqrt(len(doc_terms)))
            for term, f_td in Counter(doc_terms).items():
                if term not in self._vocabmap:
                    self._vocabmap[term] = len(self._vocabmap)
                    self._postings.append(([],[]))
                    self._docfreqs.append(0)
                term_id = self._vocabmap[term]
                self._docfreqs[term_id] += 1
                self._postings[term_id][0].append(d)
                self._postings[term_id][1].append(f_td)
        # final pass to compress the posting lists:
        for t in range(len(self._postings)):
            ds, f_tds = self._postings[t]
            self._postings[t] = (compress_with_gaps(ds), compress(f_tds))
        # TODO: compress as we CONSTRUCT the posting lists instead!

    def term_id(self, term):
        if term in self._vocabmap:
            return self._vocabmap[term]
        raise UnknownTermException(f"Unknown term: '{term}'.")
    def postings(self, term):
        # decompress posting lists on the way out:
        c_ds, c_f_tds = self._postings[self.term_id(term)]
        return idecompress_with_gaps(c_ds), idecompress(c_f_tds)
        # return self._postings[self.term_id(term)]
    def docfreq(self, term):
        return self._docfreqs[self.term_id(term)]
    def docname(self, docid):
        N = len(self._docnames)
        if docid in range(0, N):
            return self._docnames[docid]
        raise Exception(f"Invalid document id {docid} (must be in range(0,{N})")

    def query(self, q, k=10):
        """
        perform accumulator-based term-at-a-time query (sored with TFIDF)
        """
        accumulators = Counter()
        N = len(self._docnames)
        for term in q:
            if term not in self._vocabmap:
                # an unknown term t has f_t = 0 and all f_d_t = 0; Thus they 
                # contribute +0 to any document's TFIDF score! since it would
                # crash the index functions, we should skip this term!
                continue

            # otherwise, we can safely use index to calculate contributions
            # to each document's TF-IDF score from this term:
            df_t = self.docfreq(term)
            for (d, f_dt) in zip(*self.postings(term)):
                
                # The TFIDF formula we are using has two parts for each term:
                tf_factor   = math.log(1 + f_dt)
                idf_factor  = math.log(N / df_t)
                tfidf_score = tf_factor * idf_factor
                
                # Now we can add this contribution to the document's score to
                # its accumulator:
                accumulators[d] += tfidf_score

        # finally, normalise each (non-zero) scores (by sqrt document length):
        for d in accumulators:
            accumulators[d] *= self._docnorms[d]

        # now find the k with highest score
        return [(self.docname(d), s) for d, s in accumulators.most_common(k)]


class UnknownTermException(Exception):
    """For when we encounter a term not in the vocabulary."""

# # # 
# For compression/decompression:
# 

def compress(numbers):
    cbytes = bytearray()
    for number in numbers:
        vbyte_encode_into(number, cbytes)
    return bytes(cbytes)
def compress_with_gaps(numbers):
    cbytes = bytearray()
    prev_number = 0
    for number in numbers:
        gap = number - prev_number
        vbyte_encode_into(gap, cbytes)
        prev_number = number
    return bytes(cbytes)

def vbyte_encode_into(number, stream):
    # buffer of bytes for encoding this number:
    bytes_buf = bytearray([(number & 0b0111_1111) | 0b1000_0000])
    number >>= 7 # <-----.  '--------,---------'  '-----,-----'
    # starting with the lowest 7 bits, and with the end-of-number bit set on
    
    # then pump the rest of the number into the buffer, 7 low-bits at a time
    while number:
        low_bits = number & 0b0111_1111    # <=> low_bits = number  % 128
        number >>= 7                       # <=> number   = number // 128
        bytes_buf.append(low_bits)

    # reverse the buffer (for simpler/quicker decoding):    `t-,      ,e'`
    bytes_buf.reverse() #                                       \    ;    _   
                        #                                       ;   _;.-'` `s_;
    # and cast these bytes into the byte-stream! weee~'``'b.,_,y-'`'-,         
    stream.extend(bytes_buf)


def idecompress(cbytes):
    i = 0
    while i < len(cbytes):
        number, nbytes = vbyte_decode_next(cbytes, i)
        i += nbytes
        yield number
def idecompress_with_gaps(cbytes):
    prev_number = 0
    i = 0
    while i < len(cbytes):
        gap, nbytes = vbyte_decode_next(cbytes, i)
        i += nbytes
        number = prev_number + gap
        yield number
        prev_number = number

def vbyte_decode_next(stream, start):
    number = 0
    nbytes = 0

    # read in the number in 7-bit chunks
    # until we see the end-of-number bit set
    next_bits = stream[start]
    while not (next_bits & 0b1000_0000):
        number = (number << 7) | next_bits
        nbytes += 1
        next_bits = stream[start + nbytes]

    # read the last byte, without the end-of-number bit
    number = (number << 7) ^ (next_bits & 0b0111_1111)
    nbytes += 1

    # and thus, we reconstructed number, using nbytes bytes!
    return number, nbytes

