VOWELS = {"a","e","i","o","u","y"}
DOUBLE = {"bb", "dd", "ff", "gg", "mm", "nn", "pp", "rr", "tt"}
LI_END = {"c", "d", "e", "g", "h", "k", "m", "n", "r", "t"}

def stem(word):
    return _stem(word)

def _stem(word):
    """
    define and/or find:
        short syllable (CVCx or* ^VC; Cx is C - {w,x,Y})
        short word (ends in short syllable, R1 is null)
        ' regarded as a letter
    """
    if len(word) <= 2:
        return word

    # otherwise, do the following:
    word = list(word)

    r1, r2 = prepare(word)
    step_0(word, r1, r2)
    step_1(word, r1, r2)
    step_2(word, r1, r2)
    step_3(word, r1, r2)
    step_4(word, r1, r2)
    step_5(word, r1, r2)

    return "".join(word).lower()

def prepare(word):
    # remove initial ' (if present)
    # TODO: Check if we remove multiple leading '..?
    while word and word[0] == "'":
        word.pop(0)
    
    # set y in ^y or Vy to Y, left to right.
    i = len(word)
    prev_vowel = True
    for i in range(len(word)):
        if prev_vowel and word[i] == "y":
            word[i] = "Y"
        prev_vowel = word[i] in VOWELS

    # find R1, R2:
    # R1 after first VC pattern
    # R2 after second VC pattern
    r1 = None
    r2 = None
    prev_vowel = False
    for i in range(len(word)):
        if prev_vowel and word[i] not in VOWELS:
            if r1 is None:
                r1 = i+1
            else:
                r2 = i+1
                break
        prev_vowel = word[i] in VOWELS
    if r1 is None: r1 = len(word)
    if r2 is None: r2 = len(word)

    return r1, r2


def step_0(word, r1, r2):
    """
    Search for the longest among the suffixes "'", "'s", "'s'" and remove if found. 
    """
    if word and word[-1] == "'":
        word.pop()
        if word and word[-1] == "s":
            word.pop()
            if word and word[-1] == "'":
                word.pop()
    # that should do it :)

def step_1(word, r1, r2):
    step_1a(word, r1, r2)
    step_1b(word, r1, r2)
    step_1c(word, r1, r2)

def step_1a(word, r1, r2):
    """
    Search for the longest among the following suffixes, and perform the action 
    indicated.

    sses                replace by ss 
    ied   ies           replace by i if preceded by more than one letter, 
                        otherwise by ie (so ties → tie, cries → cri) 
    us    ss            do nothing
    s                   delete if the preceding word part contains a vowel not 
                        immediately before the s (so gas and this retain the s, 
                        gaps and kiwis lose it)
    """
    if word[-4:] == ["s","e","s","s"]:
        word[-4:] = ["s","s"]
    elif word[-3:] == ["i","e","d"] or word[-3:] == ["i","e","s"]:
        if len(word) > 4:
            word[-3:] = ["i"]
        else:
            word[-3:] = ["i","e"]
    elif word[-2:] == ["u","s"] or word[-2:] == ["s","s"]:
        pass
    elif word[-1:] == ["s"]:
        if any(map(VOWELS.__contains__, word[:-2])):
            word[-1:] = []
    # that should do it!

def step_1b(word, r1, r2):
    """
    Search for the longest among the following suffixes, and perform the action indicated.

    eed   eedly           replace by ee if in R1 
    ed    edly
    ing   ingly           delete if the preceding word part contains a vowel, 
                          and after the deletion: 
                            if the word ends at, bl or iz add e (so luxuriat → 
                            luxuriate), or 
                            if the word ends with a double remove the last 
                            letter (so hopp → hop), or 
                            if the word is short, add e (so hop → hope)
    """
    after = False
    if word[-5:] == ["e","e","d","l","y"]:
        if r1 >= len(word)-5:
            word[-5:] = ["e","e"]
    elif word[-3:] == ["e","e","d"]:
        if r1 >= len(word)-3:
            word[-3:] = ["e","e"]
    elif word[-5:] == ["i","n","g","l","y"]:
        if any(map(VOWELS.__contains__, word[:-5])):
            word[-5:] = []
            after = True
    elif word[-4:] == ["e","d","l","y"]:
        if any(map(VOWELS.__contains__, word[:-4])):
            word[-4:] = []
            after = True
    elif word[-3:] == ["i","n","g"]:
        if any(map(VOWELS.__contains__, word[:-3])):
            word[-3:] = []
            after = True
    elif word[-2:] == ["e","d"]:
        if any(map(VOWELS.__contains__, word[:-2])):
            word[-2:] = []
            after = True
    if after:
        if word[-2:] in [["a","t"], ["b","l"], ["i","z"]]:
            word.append("e")
        elif "".join(word[-2]) in DOUBLE:
            word.pop()
        elif is_short(word, r1): # assuming we don't cascade these rules?
            word.append("e")

def is_short(word, r1):
    if r1 < len(word):
        return False
    if len(word) == 2 and word[0] in VOWELS and word[1] not in VOWELS:
        return True
    if len(word) >= 3 and word[-3] not in VOWELS and word[-2] in VOWELS:
        if word[-1] not in VOWELS and word[-1] not in {"w","x",'Y'}:
            return True
    return False

def step_1c(word, r1, r2):
    pass
def step_2(word, r1, r2):
    pass
def step_3(word, r1, r2):
    pass
def step_4(word, r1, r2):
    pass
def step_5(word, r1, r2):
    pass
