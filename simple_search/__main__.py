from collections import Counter

from intropy import wiki

from simple_search.preproc import pre

def main():
    wiki.setup( "../../data/simple.wikipedia.org.2017.d/data.bz2"
              , "../../data/simple.wikipedia.org.2017.d/index.txt"
              )

    # load all the articles
    n_tokens = 0
    type_ids = {}
    type_cts = Counter()
    norm_documents = []
    for i, (article_name, article_raw) in enumerate(wiki.load_all(n=None)):
        print("processing", i, "-", article_name, "...")
        article = wiki.parse(article_raw).strip_code(normalize=True,collapse=True)

        # process and save this document
        article_tokens  = pre.process(article)
        article_types   = set(article_tokens)
        print(len(article_tokens), "tokens and", len(article_types), "types")
        norm_documents.append(article_tokens)

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

if __name__ == '__main__':
    main()