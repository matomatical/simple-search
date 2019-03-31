# Simple Search

A simple [Simple English Wikipedia](https://simple.wikipedia.org/wiki/Simple_English_Wikipedia) search engine.

## Run

Run package with `python3 simple_search command`, with `command` one of the following:

* `preproc`: Read the entire Simple English Wikipedia, except meta-articles (takes me just under an hour). Save pickled result into `preproc.p`.
* `index` (WIP): Will construct an inverted index based on the preprocessed documents in `preproc.p`. Will save the pickled result into `index.p`.
* `search` (Planned): Will load `index.p` and begin resolving queries entered by the user.

### Data

Oh, you would also need a bzipped dump of the Simple English Wikipedia and an associated index file (for finding articles by name in the compressed dump).

I don't provide this data right now, but this repo does contain a package `intropy` for dealing with them (this came mostly from an assignment I built while teaching COMP90059 Introduction to Programming in 2018). `intropy` was originally developed by [@noc7c9](https://github.com/noc7c9) and myself and relies on the third-party package `mwparserfromhell`.

In the future I might clean up the data API and make it easy to just download a Wikipedia dump and plug it in to this code. This could work for dumps from any Wikipedia, in principle, though the preporcessing code in this project are tailored to (simple) English.

## Goals

This project is a chance to explore ideas from COMP90042 Web Search and Text Analysis (in particular, the first couple of weeks on IR) by implementing a simple IR system myself.

While pre-existing tools abound for some of the relevant NLP tasks (most prominently, NLTK provides efficient and quality tokenisation and normalisation, and probably stop word lists, and probably more) in this project I aim to implement things, as much as possible, from *standard library Python up*, to maximise *learning and enjoyment*.

For the same reasons, this project does not aim for optimal efficiency or even complete correctness. *Tuning* and *testing* an IR system are not among my current learning goals, so I will not be spending time on these aspects. Rather, I'm building this project to *study* and *have fun*.

## Roadmap

* [x] Pre-process document collection including implementing Porter2 stemming algorithm (or close enough) (week 1, lecture 1)
* [ ] Build inverted index and implement BM25-scored term-at-a-time query algorithm (week 1, lecture 2)
* [ ] Implement index compression (vbyte) and top-k retrieval (WAND) (week 2, lecture 1)
* [ ] Catch up on week 2 and 3 lectures and add those ideas too. Incremental indexing? Query expansion and relevance feedback? Evaluation of results?

Possible extensions:

* [ ] Enhance pre-processing using ML techniques from later in the subject?
* [ ] Switch to parametric compression or some other compression. Measure speed?
* [ ] Use `Category:` pages for some kind of evaluation? (Idea: the category page provides relevance information for a query including the category name. Watch out: pages have category backlinks containing category names, which could make this too easy/inflate scores?)
* [ ] Use `#REDIRECT` articles and other links between Wikipedia pages to enhance the system using structural information (at least: link text) of structural information, to build a network.

## Notes

### Preprocessing

Not including stop-word removal (but skipping meta-articles), preprocessing took about 52 minutes and found the following statistics:

    num processed docs:    184,727
    total num tokens:   30,758,231
    total num types:       825,956

The documents / word type ID map / word count map stored in `preproc.p` was size 470MB.

#### Finding stop words

Using `simple_search/scripts/stopwords.py` I found some words with (subjectively) low information content to form a stopword list.

Notably this list includes some terms which may not usually be considered stopwords such as "categori" (category/categories), "thumb" (short for thumbnail), "birth" and "live" (many articles about people's lives, containing these words).

#### Removing redirects

I remembered from COMP90059 that some (surprisingly short) articles are actually just redirects to another article in the wikipedia! There is some probaly-relevant structural information in these redirects (the title of the redirect page could probably be incorprorated somehow into the document being pointed at) but for now I discard this information.

#### Incorporating article titles

I also decided that the article name better find its way into the article somewhere so that it will be taken into account in searching. I guess article names should be somehow weighted more strongly than article terms but for now I'm just appending them to the article.

After adding article titles to articles, and removing stopwords, here was the result of preprocessing:

    num processed docs:    138,910 (-45.8k redirects)
    total num tokens:   20,037,538 (-10.7M stop words/redirects,+titles)
    total num types:       823,191 (-2.7k from redirects?)

The size of `preproc.p` decreased to 329MB (-141MB).

### Index construction

Stay tuned!


---

Made with :purple_heart: by Matt.

Thanks to Trevor Cohn, Matthias Petri and the rest of the teaching team for putting together this subject!