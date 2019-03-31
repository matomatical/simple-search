import sys
import pickle
import textwrap

from intropy import wiki
WIKI_DATA_DIR   = "../../data/simple.wikipedia.org.2017.d"
WIKI_DATA_FILE  = WIKI_DATA_DIR + "/data.bz2"
WIKI_DATA_INDEX = WIKI_DATA_DIR + "/index.txt"
WIKI_LINK_FMT = "https://simple.wikipedia.org/wiki/{underscored_name}"

from simple_search.preproc import pre
from simple_search.index import build

PREPROC_FILE = "pickled/preproc.p"
INDEX_FILE   = "pickled/index.p"

def main():
    if not sys.argv[1:]:
        print("usage: {} command".format(sys.argv[0]),    file=sys.stderr)
        print("command is one of:",                       file=sys.stderr)
        print("  preproc: read simple english wikipedia", file=sys.stderr)
        print("  index:   construct inverted index",      file=sys.stderr)
        print("  search:  (UNDER CONSTRUCTION...)",       file=sys.stderr)
        print("  query q: (UNDER CONSTRUCTION...)",       file=sys.stderr)
        sys.exit(1)
    else:
        command = sys.argv[1]

    wiki.setup(WIKI_DATA_FILE, WIKI_DATA_INDEX)

    if command == "preproc":
        preproc()
    if command == "index":
        index()
    if command == "search":
        search()
    if command == "query":
        query(sys.argv[2:])

def preproc():
    

    # load all the articles
    documents = []
    i_all_articles = wiki.load_all(n=None, filter=non_meta)
    for i, (article_name, article) in enumerate(i_all_articles):
        print(f"processing document {i}: '{article_name}'...", end="\n ")
        article = wiki.parse(article).strip_code(normalize=True, collapse=True)
        article = str(article)
        if article.startswith("REDIRECT") or article.startswith("redirect"):
            print("↪ (redirect; skipping) ⤦")
            continue

        # process and save this document
        article_tokens  = pre.process(f"{article_name}\n\n{article}")
        documents.append((article_name, article_tokens))
        
        # output some stats
        print(f"↪ done! {len(article_tokens)} tokens.")

    save(PREPROC_FILE, documents)

    print("\nDONE!\a")
    print("num processed docs:", len(documents))
    print("total num tokens:  ", sum(map(lambda n_d: len(n_d[1]), documents)))

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
    q = input("Query (or enter to quit): ")
    while q:
        perform_query(q, index)
        q = input("Query (or enter to quit): ")
def query(args):
    if args:
        index = load(INDEX_FILE)
        perform_query(" ".join(args), index)
    else:
        print("Usage: simple_search query ENTER A QUERY HERE")

def perform_query(query, index):
    # pre-process query using same technique as document
    q = pre.process(query)

    # perform the query using index
    results = index.query(q, k=3)

    # display top few results
    print("Results:\n")
    for i, (article_name, score) in enumerate(results, 1):
        print(f"{i}. {article_name.capitalize()}")
        
        underscored_name = article_name.replace(" ", "_")
        article_link = WIKI_LINK_FMT.format(underscored_name=underscored_name)
        print(f"[{article_link}]")

        # prepare article synopsis
        article = wiki.load(article_name)
        article = wiki.parse(article).strip_code(normalize=True, collapse=True)
        print(synopsis(article))

        print()

    print("Thank you for searching!")

def synopsis(article_text, line_width=70, n_lines=3):
    lines_out = []
    for line in article_text.splitlines():
        lines_out.extend(textwrap.wrap(line, width=line_width))
        if len(lines_out) > n_lines:
            break
    if lines_out:
        # figure out where to put ellipsis
        if len(lines_out) > n_lines:
            lines_out = lines_out[:n_lines]
            if len(lines_out[-1]) <= line_width - 3:
                lines_out[-1] += "..."
            else:
                lines_out[-1] = lines_out[-1][:-3] + "..."

        return "\n".join(lines_out)
    else:
        return "[no text]"


def load(pfile):
    print(f"loading {pfile}...", end=" ", flush=True)
    with open(pfile, "rb") as pickle_jar:
        data = pickle.load(pickle_jar)
    print("loaded!")
    return data
def save(pfile, data):
    print("saving...", end=" ", flush=True)
    with open(pfile, "wb") as pickle_jar:
        pickle.dump(data, pickle_jar)
    print(f"saved to {pfile}!")



if __name__ == '__main__':
    main()