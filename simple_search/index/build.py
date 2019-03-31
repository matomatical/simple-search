"""
Module provides classes and functions for dealing with 

"""

from collections import Counter

class SimpleIndex:
    def __init__(self, documents):
        self._vocabmap = {} # term t -> t's term id
        self._postings = [] # t's term id -> ([d], [f_t,d]) | d <- ds, f_t,d > 0
        self._docfreqs = [] # t's term id -> df_t
        self._docnames = [] # d -> d's name (for lookup in collection)
        
        for d, (doc_name, doc_terms) in enumerate(documents):
            self._docnames.append(doc_name)
            for term, f_td in Counter(doc_terms).items():
                if term not in self._vocabmap:
                    self._vocabmap[term] = len(self._vocabmap)
                    self._postings.append(([],[]))
                    self._docfreqs.append(0)
                term_id = self._vocabmap[term]
                self._docfreqs[term_id] += 1
                self._postings[term_id][0].append(d)
                self._postings[term_id][1].append(f_td)
        # compress the posting lists on the way in:
        for t in range(len(self._postings)):
            ds, f_dts = self._postings[t]
            self._postings[t] = (compress_with_gaps(ds), compress(f_dts))

    def term_id(self, term):
        if term in self._vocabmap:
            return self._vocabmap[term]
        raise UnknownTermException(f"Unknown term: '{term}'.")
    def postings(self, term):
        # decompress posting lists on the way out:
        c_ds, c_f_dts = self._postings[self.term_id(term)]
        return idecompress_with_gaps(c_ds), idecompress(c_f_dts)
    def docfreq(self, term):
        return self._docfreqs[self.term_id(term)]
    def docname(self, docid):
        N = len(self._docnames)
        if docid in range(0, N):
            return self._docnames[docid]
        raise Exception(f"Invalid document id {docid} (must be in range(0,{N})")

class UnknownTermException(Exception):
    """For when we encounter a term not in the vocabulary."""

# # # 
# For compression/decompression:
# 

def compress(numbers):
    cbytes = bytearray()
    for number in numbers:
        vbyte_encode_into(number, cbytes)
    return cbytes
def compress_with_gaps(numbers):
    cbytes = bytearray()
    prev_number = 0
    for number in numbers:
        gap = number - prev_number
        vbyte_encode_into(gap, cbytes)
    return cbytes

def idecompress(cbytes):
    i = 0
    while i < len(cbytes):
        nbytes, number = vbyte_decode_next(cbytes, i)
        i += nbytes
        yield number
def idecompress_with_gaps(cbytes):
    prev_number = 0
    i = 0
    while i < len(cbytes):
        nbytes, gap = vbyte_decode_next(cbytes, i)
        i += nbytes
        number = prev_number + gap
        yield number
        prev_number = number

def vbyte_encode_into(number, stream):    
    # buffer of bytes for encoding this number:
    bytes_buf = bytearray([(number & 0b0111_1111) ^ 0b1000_0000])
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

def vbyte_decode_next(stream, start):
    number = 0
    nbytes = 0

    # read in the number in 7-bit chunks
    # until we see the end-of-number bit set
    next_bits = stream[start]
    while not (next_bits & 0b1000_0000):
        number = (number << 7) ^ next_bits
        nbytes += 1
        next_bits = stream[start + nbytes]

    # read the last byte, without the end-of-number bit
    number = (number << 7) ^ (next_bits & 0b0111_1111)
    nbytes += 1

    # and thus, we reconstructed number, using nbytes bytes!
    return number, nbytes

# TODO: TEST COMPRESSION