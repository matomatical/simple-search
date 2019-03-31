"""
Various scoring functions for ranking documents
"""

def tfidf_contrib(term, document):
    return 0 # TODO
def bm25_contrib(term, document):
    return 0 # TODO

class Score:
    TFIDF = tfidf_contrib
    BM25  = bm25_contrib
    OKAPI = BM25 # synonym

