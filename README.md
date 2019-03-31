# *Simple Search*

A simple [Simple English Wikipedia](https://simple.wikipedia.org/wiki/Simple_English_Wikipedia) search engine.

## Run

Run package with `python3 simple_search command`, with `command` one of the following:

* `preproc`: Read the entire Simple English Wikipedia, except meta-articles (takes me just under an hour). Save pickled result into `preproc.p`.
* `index` (WIP): Will construct an inverted index based on the preprocessed documents in `preproc.p`. Will save the pickled result into `index.p`.
* `search` (Planned): Will load `index.p` and begin resolving queries entered by the user.

### Data

Oh, you would also need a bzipped dump of the Simple English Wikipedia and an associated index file (for finding articles by name in the compressed dump).

I don't provide this data right now, but this repo does contain a package `intropy` for dealing with them (this came mostly from an assignment I built while teaching COMP90059 Introduction to Programming in 2018). `intropy` was originally developed by [@noc7c9](https://github.com/noc7c9) and myself and relies on the third-party package `mwparserfromhell`.

## Goals

This project is a chance to explore ideas from COMP90042 Web Search and Text Analysis (in particular, the first couple of weeks on IR) by implementing a simple IR system myself.

While pre-existing tools abound for some of the relevant NLP tasks (most prominently, NLTK provides efficient and quality tokenisation and normalisation, and probably stop word lists, and probably more) in this project I aim to implement things, as much as possible, from *standard library Python up*, to maximise *learning and enjoyment*.

For the same reasons, this project does not aim for optimal efficiency or even complete correctness. *Tuning* and *testing* an IR system are not among my current learning goals, so I will not be spending time on these aspects. Rather, I'm building this project to *study* and *have fun*.

## Roadmap

* [ ] Pre-process document collection including implementing Porter2 stemming algorithm (or close enough) (week 1, lecture 1)
* [ ] Build inverted index and implement BM25-scored term-at-a-time query algorithm (week 1, lecture 2)
* [ ] Implement index compression (vbyte) and top-k retrieval (WAND) (week 2, lecture 1)
* [ ] Catch up on week 2 and 3 lectures and add those ideas too. Incremental indexing? 

Possible extensions:

* [ ] Enhance pre-processing using ML techniques from later in the subject?
* [ ] Switch to parametric compression or some other compression. Measure speed?
* [ ] Use `Category:` pages for some kind of evaluation? (Idea: the category page provides relevance information for a query including the category name. Watch out: pages have category backlinks, which could make this too easy?)

## Notes

### Preprocessing

Not including stop-word removal (but skipping meta-articles), preprocessing took about 52 minutes and found the following statistics:

    num processed docs: 184727
    total num tokens:   30758231
    total num types:    825956

The documents / word type ID map / word count map stored in `preproc.p` was size 470MB.

#### Finding stop words

Using `simple_search/scripts/stopwords.py` I found some words with (subjectively) low information content to form a stopword list.

Notably this list includes some terms which may not usually be considered stopwords such as "categori" (category/categories), "thumb" (short for thumbnail), "birth" and "live" (many articles about people's lives, containing these words).

Hey that reminds me... I should remove articles that are just a redirect to another article!


#### Incorporating article titles

I also decided that the article name better find its way into the article somewhere so that it will be taken into account in searching. I guess article names should be somehow weighted more strongly than article terms but for now I'm just appending them to the article.

After adding article titles to articles, and removing stopwords, here was the result of preprocessing:

    num processed docs: ? (-0)
    total num tokens:   ? (-?)
    total num types:    ? (-?)

The size of `preproc.p` decreased to ?MB.

---

Made with :purple_heart: by Matt.

Thanks to Trevor Cohn, Matthias Petri and the rest of the teaching team for putting together this subject!