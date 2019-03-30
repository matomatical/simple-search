from intropy import wiki
from simple_search.preproc import pre

def main():
    wiki.setup( "../../data/simple.wikipedia.org.2017.d/data.bz2"
              , "../../data/simple.wikipedia.org.2017.d/index.txt"
              )
    article = wiki.parse(wiki.load("Alan Turing")) \
                  .strip_code(normalize=True, collapse=True)
    tokens  = pre.process(article)
    types   = set(tokens)

    print(tokens)
    print(types)

if __name__ == '__main__':
    main()