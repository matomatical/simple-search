import re

from intropy import wiki
wiki.setup("../../data/simple.wikipedia.org.2017.d/data.bz2","../../data/simple.wikipedia.org.2017.d/index.txt")

from porter2 import stem

def main():
    article = wiki.parse(wiki.load("Alan Turing"))

    # remove unwanted formatting information:
    article = str(article.strip_code(normalize=True, collapse=True))
    article = re.sub(r"<[^>]*>", " ", article)

    # segment structure:
    pass # is this necessary for IR?

    # tokenise words:
    # [\w\d'\-\.]+
    words = re.split(r"[^\w\d'\-\.]+", article, flags=re.UNICODE)
    words = [word.replace(".","") for word in words]
    words = [word for word in words if word]

    # normalise words:
    words = [normalise(word) for word in words]

    # remove unwanted words:
    words = [word for word in words if not stop(word)]

    print(words)

STOPWORDS = set()
def stop(word):
    return word in STOPWORDS

def normalise(word):
    return stem(word)

if __name__ == '__main__':
    main()