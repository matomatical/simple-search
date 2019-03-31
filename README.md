# *Simple Search*

A simple (Simple English Wikipedia)[https://simple.wikipedia.org/wiki/Simple_English_Wikipedia] search engine.

## Run

Run package with `python3 simple_search`. (Currently, this preprocesses documents).

### Data

Oh, you would also need a bzipped dump of the Simple English Wikipedia and an associated index file (for finding articles by name in the compressed dump).

I don't provide this data right now, but this repo does contain a package `intropy` for dealing with them (this came mostly from an assignment I built while teaching COMP90059 Introduction to Programming in 2018). `intropy` was originally developed by (@noc7c9)[https://github.com/noc7c9] and myself and relies on the third-party package `mwparserfromhell`.

## Goals

This project is a chance to explore ideas from COMP90042 Web Search and Text Analysis (in particular, the first couple of weeks on IR) by implementing a simple IR system myself.

While pre-existing tools abound for some of the relevant NLP tasks (most prominently, NLTK provides efficient and quality tokenisation and normalisation, and probably stop word lists, and probably more) in this project I aim to implement things, as much as possible, from *standard library Python up*, to maximise *learning and enjoyment*.

For the same reasons, this project does not aim for optimal efficiency or even complete correctness. *Tuning* and *testing* an IR system are not among my current learning goals, so I will not be spending time on these aspects. Rather, I'm building this project to *study* and *have fun*.

## Roadmap

[ ] Pre-process document collection including implementing Porter2 stemming algorithm (or close enough) (week 1, lecture 1)
[ ] Build inverted index and implement BM25-scored term-at-a-time query algorithm (week 1, lecture 2)
[ ] Implement index compression (vbyte) and top-k retrieval (WAND) (week 2, lecture 1)
[ ] Catch up on week 2 and 3 lectures and add those ideas too. Incremental indexing? 

Possible extensions:

[ ] Enhance pre-processing using ML techniques from later in the subject?
[ ] Switch to parametric compression or some other compression. Measure speed?
[ ] Use `Category:` pages for some kind of evaluation? (Idea: the category page provides relevance information for a query including the category name. Watch out: pages have category backlinks, which could make this too easy?)
---

Made with :purple_heart: by Matt.

Thanks to Trevor Cohn, Matthias Petri and the rest of the teaching team for putting together this subject!