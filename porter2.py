"""
Implement a simplified version of the Snowball English (Porter2) stemmer.
(Simplified because it doesn't currently handle exceptional forms. It's also
untested and so should not be considered correct.)

Usage:

>>> from porter2 import stem
>>> stem(word)                                          # no need to .lower()
"""


# Define a vowel as one of
_VOWELS = {"a","e","i","o","u","y"}

# Define a double as one of
_DOUBLE = {"bb", "dd", "ff", "gg", "mm", "nn", "pp", "rr", "tt"}

# Define a valid li-ending as one of 
_LI_END = {"c", "d", "e", "g", "h", "k", "m", "n", "r", "t"}

def stem(word):
    return Stemmer(word).stem

class Stemmer:
    def __init__(self, word):
        """lowercase and stem `word`."""
        self.stem = word.lower()
        self.s = list(word.lower())
        if len(self.s) <= 2:
            # If the word has two letters or less, leave it as it is.
            pass  
        else:
            # Otherwise, do each of the following operations:
            self.prepare() # prepare ys, calculate r1, r2, etc.
            self.step0()
            self.step1a()
            self.step1b()
            self.step1c()
            self.step2()
            self.step3()
            self.step4()
            self.step5()
            # Finally, turn any remaining Y letters in the word back into lower
            # case.
            self.stem = "".join(self.s).lower()

    def prepare(self):
        # remove initial 's (if present)
        while self.s and self.s[0] == "'":
            self.s.pop(0)
        
        # set y in ^y or Vy to Y, left to right.
        i = len(self.s)
        prev_vowel = True
        for i in range(len(self.s)):
            if prev_vowel and self.s[i] == "y":
                self.s[i] = "Y"
            prev_vowel = self.s[i] in _VOWELS

        # R1 is the region after the first non-vowel following a vowel, or the
        # end of the word if there is no such non-vowel.
        # R2 is the region after the first non-vowel following a vowel in R1,
        # or the end of the word if there is no such non-vowel.
        self.r1 = None
        self.r2 = None
        prev_vowel = False
        for i in range(len(self.s)):
            if prev_vowel and self.s[i] not in _VOWELS:
                # found a VC
                if self.r1 is None:
                    self.r1 = i+1
                else:
                    # found a second VC
                    self.r2 = i+1
                    break # no more needed
            prev_vowel = self.s[i] in _VOWELS
        if self.r1 is None:
            self.r1 = len(self.s)
        if self.r2 is None:
            self.r2 = len(self.s)

    def step0(self):
        """
        Search for the longest among the following suffixes, and perform the 
        action indicated.
        '   's    's':     remove
        """
        if self.ends("'"):
            self.delete()
        if self.ends("'s"):
            self.delete()

    def step1a(self):
        """
        Search for the longest among the following suffixes, and perform the 
        action indicated.

        sses:          replace by ss
        ied+   ies*:   replace by i if preceded by more than one letter, 
                       otherwise by ie (so ties -> tie, cries -> cri)
        us+   ss:      do nothing
        s:             delete if the preceding word part contains a vowel not 
                       immediately before the s (so gas and this retain the s, 
                       gaps and kiwis lose it)
        """        
        if self.ends("sess"):
            self.replace("ss")
        elif self.ends("ied") or self.ends("ies"):
            if len(self.s) > 4:
                self.replace("i")
            else:
                self.replace("ie")
        elif self.ends("us") or self.ends("ss"):
            pass
        elif self.ends("s"):
            # delete if the preceding word part contains a vowel not
            # immediately before the s:
            delete = False
            for i in range(0, len(self.s)-2): # skip last + 2nd last letter
                if self.s[i] in _VOWELS:
                    delete = True
                    break
            if delete:
                self.delete()
        # that should do it!

    def step1b(self):
        """
        Search for the longest among the following suffixes, and perform the 
        action indicated.

        eed   eedly+:                replace by ee if in R1
   
        ed   edly+   ing   ingly+:   delete if the preceding word part contains 
                                     a vowel, and after the deletion: 
                                        * if the word ends at, bl or iz add e
                                          (so luxuriat -> luxuriate), OR 
                                        * if the word ends with a double remove 
                                          the last letter (so hopp -> hop), OR 
                                        * if the word is short, add e
                                          (so hop -> hope)
        """
        if self.ends("eedly") or self.ends("eed"):
            if self.region() >= 1:
                self.replace("ee")
        elif self.ends("ingly") or self.ends("edly") or self.ends("ed") \
                                                    or self.ends("ing"):
            delete = False
            for i in range(0, len(self.s)-2): # skip last + 2nd last letter
                if self.s[i] in _VOWELS:
                    delete = True
                    break
            if delete:
                self.delete()
                if self.ends("at") or self.ends("bl") or self.ends("iz"):
                    self.add("e")
                elif "".join(self.s[-2:]) in _DOUBLE:
                    self.s.pop()
                elif self.short():
                    self.add("e")
    def step1c(self):
        """
        Replace suffix y or Y by i if preceded by a non-vowel which is not the 
        first letter of the word (so cry -> cri, by -> by, say -> say)
        """
        if self.ends("y") or self.ends("Y"):
            if len(self.s) > 2 and self.s[-2] not in _VOWELS:
                self.replace("i")

    def step2(self):
        """
        Search for the longest among the following suffixes, and, if found and 
        in R1, perform the action indicated.

        (this order should work:)

        izer:      replace by ize
        ization:   replace by ize 
        ation:     replace by ate
        ator:      replace by ate
        ational:   replace by ate
        tional:    replace by tion
        iveness:   replace by ive
        iviti:     replace by ive
        enci:      replace by ence
        anci:      replace by ance
        fulness:   replace by ful
        ogi+:      replace by og if preceded by l
        alism:     replace by al
        aliti:     replace by al
        alli:      replace by al
        abli:      replace by able
        ousness:   replace by ous
        ousli:     replace by ous
        biliti:    replace by ble
        bli+:      replace by ble
        entli:     replace by ent
        fulli+:    replace by ful
        lessli+:   replace by less
        
        li+:       delete if preceded by a valid li-ending
        """
        if self.ends("izer") or self.ends("ization"): # what about iSation etc.?
            if self.region() >= 1: self.replace("ize")
        elif self.ends("ator") or self.ends("ation") or self.ends("ational"):
            if self.region() >= 1: self.replace("ate")
        elif self.ends("tional"):
            if self.region() >= 1: self.replace("tion")
        elif self.ends("iveness") or self.ends("iviti"):
            if self.region() >= 1: self.replace("ive")
        elif self.ends("enci"):
            if self.region() >= 1: self.replace("ence")
        elif self.ends("anci"):
            if self.region() >= 1: self.replace("ance")
        elif self.ends("fulness"):
            if self.region() >= 1: self.replace("ful")
        elif self.ends("ogi"):
            if self.region() >= 1:
                # why isn't this the initial rule? probably something about the
                # order of the r1 check.
                if self.ends("logi"): self.replace("log")
        # must check before li:
        elif self.ends("alism") or self.ends("aliti") or self.ends("alli"):
            if self.region() >= 1: self.replace("al")
        elif self.ends("abli"):
            if self.region() >= 1: self.replace("able")
        elif self.ends("ousness") or self.ends("ousli"):
            if self.region() >= 1: self.replace("ous")
        elif self.ends("biliti") or self.ends("bli"):
            if self.region() >= 1: self.replace("ble")
        elif self.ends("entli"):
            if self.region() >= 1: self.replace("ent")
        elif self.ends("fulli"):
            if self.region() >= 1: self.replace("ful")
        elif self.ends("lessli"):
            if self.region() >= 1: self.replace("less")
        elif self.ends("li"):
            if self.region() >= 1:
                # delete if preceded by a valid li-ending
                if len(self.s) > 2 and self.s[-3] in _LI_END:
                    self.delete()
        
    def step3(self):
        """
        Search for the longest among the following suffixes, and, if found and 
        in R1, perform the action indicated.

        ational+:               replace by ate
        tional+:                replace by tion
        alize:                  replace by al
        icate   iciti   ical:   replace by ic
        ful   ness:             delete
        ative*:                 delete if in R2 
        """
        if self.ends("ational"):
            if self.region() >= 1: self.replace("ate")
        elif self.ends("tional"):
            if self.region() >= 1: self.replace("tion")
        elif self.ends("alize"):
            if self.region() >= 1: self.replace("al")
        elif self.ends("icate") or self.ends("iciti") or self.ends("ical"):
            if self.region() >= 1: self.replace("ic")
        elif self.ends("ful") or self.ends("ness"):
            if self.region() >= 1: self.delete()
        elif self.ends("ative"):
            if self.region() == 2: self.delete()
    
    def step4(self):
        """
        Search for the longest among the following suffixes, and, if found and 
        in R2, perform the action indicated.

        al   ance   ence   er   ic   able
        ible   ant   ement   ment   ent
        ism   ate   iti   ous   ive   ize:   delete 
        ion:                                 delete if preceded by s or t 
        """
        for suffix in [ "ement", "ment", "ent"
                      , "ance", "ence", "able", "ible"
                      , "ant", "ate", "ism", "iti", "ive", "ize", "ous"
                      , "al", "er", "ic"
                      ]:
            if self.ends(suffix):
                if self.region() == 2:
                    self.delete()
                # HMMM!? Do I break here or one level below (incase the first
                # match found is not in r2?) the wording suggests to do it this
                # way.
                break
        if self.ends("ion"):
            if self.region() == 2:
                if len(self.s) > 2 and self.s[-3] in {'s', 't'}:
                    self.delete()

    def step5(self):
        """
        Search for the following suffixes, and, if found, perform the action 
        indicated.

        e:    delete if in R2, or in R1 and not preceded by a short syllable 
        l:    delete if in R2 and preceded by l 
        """
        if self.ends("e"):
            r = self.region()
            if r == 2 or (r == 1 and not self.end_short_syl()):
                self.delete()
        elif self.ends("l"):
            r = self.region()
            if r == 2:
                if len(self.s) > 1 and self.s[-2] == 'l':
                    self.delete()

    def ends(self, suffix):
        """Do we currently end with this suffix? (If so, sets the mark)"""
        l = len(suffix)
        if self.s[-l:] == list(suffix):
            # we DO end with this suffix! set the mark and return.
            self.mark = len(self.s)-l
            return True
        # we do NOT end with this suffix! leave the mark and return.
        return False
    def delete(self):
        # we no longer want whatever is after the mark:
        self.s[self.mark:] = []
    def replace(self, new_suffix):
        # we no longer want whatever is after the mark,
        # we want new_suffix there instead!
        self.s[self.mark:] = list(new_suffix)
    def add(self, new_suffix):
        # we do want whatever is after the mark, but also to add
        # this new_suffix there too!
        self.s.extend(list(new_suffix))

    def region(self):
        """In which region is the mark?"""
        if self.mark < self.r1:
            return 0
        elif self.mark < self.r2:
            return 1
        else:
            return 2
    def end_short_syl(self, end=None):
        """
        Method: Is there a short syllable right `end` (default: the mark)?

        Define a short syllable in a word as either
            (a) a vowel followed by a non-vowel other than w, x or Y and 
                preceded by a non-vowel, OR
            *(b) a vowel at the beginning of the word followed by a non-vowel. 

        So rap, trap, entrap end with a short syllable, and ow, on, at are 
        classed as short syllables. But uproot, bestow, disturb do not end 
        with a short syllable.
        """
        if end is None: end = self.mark
        # (a)
        if self.mark > 2 \
                and self.s[end-2] in _VOWELS \
                and self.s[end-1] not in (_VOWELS | {'w','x','Y'}) \
                and self.s[end-3] not in _VOWELS:
            return True
        # (b)
        elif end == 2 \
                and self.s[0] in _VOWELS \
                and self.s[1] not in _VOWELS:
            return True        
        return False

    def short(self):
        """
        A word is called short if it ends in a short syllable, and if R1 is 
        null.
        """
        #       r1 null:                    a short syllable at the end
        return (self.r1 >= len(self.s)) and self.end_short_syl(end=len(self.s))
