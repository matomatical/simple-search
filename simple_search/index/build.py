"""
Module provides classes and functions for dealing with 

"""

from collections import Counter

# from simple_search.index.code import Code
# from simple_search.index.score import Score

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
        # TODO: Compress postsings (here, after index is loaded)

    def term_id(self, term):
        if term in self._vocabmap:
            return self._vocabmap[term]
        raise UnknownTermException(f"Unknown term: '{term}'.")
    def postings(self, term):
        return self._postings[self.term_id(term)]
    def docfreq(self, term):
        return self._docfreqs[self.term_id(term)]
    def docname(self, docid):
        N = len(self._docnames)
        if docid in range(0, N):
            return self._docnames[docid]
        raise Exception(f"Invalid document id {docid} (must be in range(0,{N})")


class UnknownTermException(Exception):
    """For when we encounter a term not in the vocabulary."""


