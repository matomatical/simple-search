# *Simple Search*, a simple Simple English Wikipedia search engine

Run package with `python3 simple_search`.

## Goals

This project is a chance to practice ideas learned from COMP90042 Web Search and Text Analysis (in particular, the first couple of weeks on IR) by implementing them myself.

Pre-existing tools abound for some of the relevant NLP tasks including NLTK (particularly tokenisation and normalisation) and stop word lists, etc. Regardless, in this project I want to implement things, as much as possible, from *standard library Python up*, to maximise *learning and fun*.

For the same reasons, this project does not aim for optimal efficiency or even complete correctness or efficiency. Learning about how to *tune* and *test* IR systems are not among my current learning goals, so I will not be spending time on these aspects. Rather, I'm building this project to *study* and *have fun*.

## Roadmap

Currently pre-processes documents and that's all.

[ ] Pre-process document collection including implementing Porter2 stemming algorithm (or close enough) (week 1, lecture 1)
[ ] Build inverted index and implement BM25-scored term-at-a-time query algorithm (week 1, lecture 2)
[ ] Implement index compression (vbyte) and top-k retrieval (WAND) (week 2, lecture 1)
[ ] Catch up on week 2 and 3 lectures and add those ideas too. Incremental indexing? 

Possible extensions:

[ ] Enhance pre-processing using ML techniques from later in the subject?
[ ] Switch to parametric compression

---

Made with :purple_heart: by Matt.

Thanks to Trevor Cohn, Matthias Petri and the rest of the teaching team for putting together this subject!