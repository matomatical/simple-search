# Simple Search

A simple [Simple English Wikipedia](https://simple.wikipedia.org/wiki/Simple_English_Wikipedia) search engine.

## Run

Run package with `python3 simple_search command`, with `command` one of the following:

1. `preproc`: Read and process the entire Simple English Wikipedia, except meta-articles and redirects. Save pickled result into `preproc.p`. Takes me around 50 minutes.
2. `index`: Construct an inverted index based on the preprocessed documents in `preproc.p`. Save the pickled result into `index.p`.
3. `search`: Loads `index.p` and begin resolving queries entered interactively by the user.
4. `query`: Loads `index.p` to resolve a one-time query from the command line.

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
* [ ] Build inverted index and implement TFIDF- and BM25-scored term-at-a-time query algorithm (week 1, lecture 2)
    * [x] tfidf
    * [ ] bm25
* [ ] Implement index compression (vbyte) and top-k retrieval (WAND) (week 2, lecture 1)
    * [x] vbyte compression
    * [ ] top-k retrieval
* [ ] Catch up on week 2 and 3 lectures and add those ideas too. Incremental indexing? Query expansion and relevance feedback? Evaluation of results?

Possible extensions:

* [ ] Switch to block-based compression/decompression and block max WAND.
* [ ] Enhance pre-processing using ML techniques from later in the subject?
* [ ] Consider parametric compression or some other compression (delta?). Evaluate by measuring space/speed tradeoff?
* [ ] Use `Category:` pages for some kind of evaluation? (Idea: the category page provides relevance information for a query including the category name. Watch out: pages have category backlinks containing category names, which could make this too easy/inflate scores?)
* [ ] Use `#REDIRECT` articles and other links between Wikipedia pages to enhance the system using structural information (at least: link text) of structural information, to build a network.
* [ ] Apply incremental indexing techiques to processing the regular English Wikipedia..!?
* [ ] Take what I learn about streaming graph algorithms next semester and apply to processing the regular English Wikipedia's structure!?

## Notes

### Preprocessing

Not including stop-word removal (but skipping meta-articles), preprocessing took about 52 minutes and found the following statistics:

    num processed docs:    184,727
    total num tokens:   30,758,231

The documents / word type ID map / word count map stored in `preproc.p` was size 470MB.

#### Finding stop words

Using `simple_search/scripts/stopwords.py` I found some words with (subjectively) low information content to form a stopword list.

Notably this list includes some terms which may not usually be considered stopwords such as "categori" (category/categories), "thumb" (short for thumbnail), "birth" and "live" (many articles about people's lives, containing these words).

#### Removing redirects

I remembered from COMP90059 that some (surprisingly short) articles are actually just redirects to another article in the wikipedia! There is some probaly-relevant structural information in these redirects (the title of the redirect page could probably be incorprorated somehow into the document being pointed at) but for now I discard this information.

#### Incorporating article titles

I also decided that the article name better find its way into the article somewhere so that it will be taken into account in searching. I guess article names should be somehow weighted more strongly than article terms but for now I'm just appending them to the article.


After adding article titles to articles, skipping redirects, and removing stopwords, here is the result of preprocessing:

    num processed docs:    132,640 (-52.0k redirects)
    total num tokens:   20,013,232 (-10.7M stop words/redirects/+titles)

The size of `preproc.p` decreased to 314MB (-155MB).

### Index construction

The index consists of:

* One pair of posting lists (document ids and corresponding term document frequencies) for each of ~823k terms.
* One document frequency count for each of ~823k terms (coinciding with the length of the posting lists, but only until we store the latter compressed).
* A map of terms (strings) to term ids; the remaining lists are indexed by these term ids to save space and time.
* A map of document ids (as found in posting lists) to document names (strings, to be used for looking up articles in the Wikipedia).

Before compression, the pickled index is 110MB in size and takes about 36 seconds to build.

### Variable-byte encoding the posting lists

I reimplemented my vbyte encoding functions from the homework and added posting list compression to the index. Now it takes... 1 minute and 14 seconds. Here are the size results:

    size of _docnames:       3.50MB
    size of _docfreqs:       1.65MB
    size of _vocabmap:      20.15MB
    size of _postings:      59.85MB (-25.38MB, from 85.23MB uncompressed)
    size of index file:     85.16MB (-25.38MB, from 110.53MB uncompressed)

#### Profiling memory footprint

It seems Python is actually pretty efficient at serialising integer lists. Also, the integers in my posting lists are relatively small already. I wonder if savings are greter while the lists are in-memory?

Profiling with `psutil` seems to suggest that the index takes up 500-600MB in memory, and is only decreased by about 50MB using this compression... That doesn't really add up, so there must be some trickery going on within Python itself. Alas, this is where my analysis will end.

---

Made with :purple_heart: by Matt.

Thanks to Trevor Cohn, Matthias Petri and the rest of the teaching team for putting together this subject!