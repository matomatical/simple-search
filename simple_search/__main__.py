import sys
import pickle
from collections import Counter

from intropy import wiki

from simple_search.preproc import pre

def main():
    if not sys.argv[1:]:
        print("usage: {} command".format(sys.argv[0]),    file=sys.stderr)
        print("command is one of:",                       file=sys.stderr)
        print("  preproc: read simple english wikipedia", file=sys.stderr)
        print("  index:   construct inverted index",      file=sys.stderr)
        print("  (more to come...)",                      file=sys.stderr)
        sys.exit(1)
    else:
        command = sys.argv[1]

    if command == "preproc":
        preproc()
    if command == "index":
        index()

def preproc():
    wiki.setup( "../../data/simple.wikipedia.org.2017.d/data.bz2"
              , "../../data/simple.wikipedia.org.2017.d/index.txt"
              )

    # load all the articles
    n_tokens = 0
    type_ids = {}
    type_cts = Counter()
    norm_documents = []
    i_all_articles = wiki.load_all(n=None, filter=non_meta)
    for i, (article_name, article_raw) in enumerate(i_all_articles):
        print("processing", i, "-", article_name, "...")
        article = wiki.parse(article_raw).strip_code(normalize=True,collapse=True)

        # process and save this document
        article_tokens  = pre.process(article)
        article_types   = set(article_tokens)
        print(len(article_tokens), "tokens and", len(article_types), "types")
        norm_documents.append((article_name, article_tokens))

        # add to vocab and counts
        n_tokens += len(article_tokens)
        type_cts.update(article_tokens)
        for word in article_types:
            if word not in type_ids:
                type_ids[word] = len(type_ids)

    print("\nDONE!\a")
    print("num processed docs:", len(norm_documents))
    print("total num tokens:  ", n_tokens)
    print("total num types:   ", len(type_ids))

    print("SAVING:")
    
    with open("preproc.p", "wb") as pickle_jar:
        pickle.dump((norm_documents, type_ids, type_cts), pickle_jar)

def non_meta(name):
    return (":" not in name) or (": " in name)

def index():
    print("LOADING:")
    with open("preproc.p", "rb") as pickle_jar:
        (norm_documents, type_ids, type_cts) = pickle.load(pickle_jar)
    print("num processed docs:", len(norm_documents))
    print("total num tokens:  ", sum(type_cts.values()))
    print("total num types:   ", len(type_ids))

if __name__ == '__main__':
    main()