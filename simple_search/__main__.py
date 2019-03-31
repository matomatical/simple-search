import sys
import pickle

from intropy import wiki

from simple_search.preproc import pre
from simple_search.index import build

PREPROC_FILE = "preproc.p"
INDEX_FILE   = "index.p"

def main():
    if not sys.argv[1:]:
        print("usage: {} command".format(sys.argv[0]),    file=sys.stderr)
        print("command is one of:",                       file=sys.stderr)
        print("  preproc: read simple english wikipedia", file=sys.stderr)
        print("  index:   construct inverted index",      file=sys.stderr)
        print("  search:  (UNDER CONSTRUCTION...)",       file=sys.stderr)
        print("  query:   (UNDER CONSTRUCTION...)",       file=sys.stderr)
        sys.exit(1)
    else:
        command = sys.argv[1]

    if command == "preproc":
        preproc()
    if command == "index":
        index()
    if command == "search":
        search()
    if command == "query":
        query()

def preproc():
    wiki.setup( "../../data/simple.wikipedia.org.2017.d/data.bz2"
              , "../../data/simple.wikipedia.org.2017.d/index.txt"
              )

    # load all the articles
    documents = []
    i_all_articles = wiki.load_all(n=None, filter=non_meta)
    for i, (article_name, article) in enumerate(i_all_articles):
        print(f"processing document {i}: '{article_name}'...", end="\n ")
        article = wiki.parse(article).strip_code(normalize=True, collapse=True)
        article = str(article)
        if article.startswith("REDIRECT"):
            print("↪ (redirect; skipping) ⤦")
            continue

        # process and save this document
        article_tokens  = pre.process(f"{article_name}\n\n{article}")
        documents.append((article_name, article_tokens))
        
        # output some stats
        print(f"↪ done! {len(article_tokens)} tokens.")


    print("\nDONE!\a")
    print("num processed docs:", len(documents))
    print("total num tokens:  ", sum(map(lambda n_d: len(d), documents)))

    save(PREPROC_FILE, documents)

def non_meta(name):
    return (":" not in name) or (": " in name)

def index():
    documents = load(PREPROC_FILE)

    print("inverting documents...", end=" ", flush=True)
    index = build.SimpleIndex(documents)
    print("done!")

    save(INDEX_FILE, index)



def search():
    index = load(INDEX_FILE)

def load(pfile):
    print(f"loading {pfile}...", end=" ", flush=True)
    with open(pfile, "rb") as pickle_jar:
        data = pickle.load(pickle_jar)
    print("loaded!")
    return data
def save(pfile, data):
    print("saving...", end=" ", flush=True)
    with open(pfile, "wb") as pickle_jar:
        pickle.dump(pickle_jar, data)
    print(f"saved to {pfile}!")




    

if __name__ == '__main__':
    main()