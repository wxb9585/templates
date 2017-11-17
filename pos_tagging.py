# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    single = set()
    plural = set()
    unchange = []
    with open("sentences.txt", "r") as f:
        for line in f:
            # add code here
            for wordtag in line.split():
                if wordtag.split('|')[1] == "NN":
                    single.add(wordtag.split('|')[0])
                elif wordtag.split('|')[1] == "NNS":
                    plural.add(wordtag.split('|')[0])

    for check in single:
        if check in plural:
            unchange.append(check)

    return unchange

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    # add code here
    if s in unchanging_plurals_list:
        return s
    elif re.match (".*men$",s):
        snew = s[:-3] + "man"
    elif re.match(".*[aeiou]ys$",s):
        snew = s[:-1]
    elif re.match(".*([^sxyzaeiou]|[^cs]h)s$",s):
        snew = s[:-1]
    elif re.match("[^aeiou]ies$",s):
        snew = s[:-1]
    elif re.match(".*[^s]ses$",s):
        snew = s[:-1]
    elif re.match(".*[^z]zes$",s):
        snew = s[:-1]
    elif re.match(".*([^iosxzh]|[^cs]h)es$",s):
        snew = s[:-1]
    elif len(s)>=5 and re.match(".*[^aeiou]ies$",s):
        snew = s[:-3] + 'y'
    elif re.match(".*([ox]|[cs]h|ss|zz)es$",s):
        snew = s[:-2]
    else:
        snew = ""
    return snew
def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here
    tagOfWord = []
    if wd in function_words:
        for t in function_words_tags:
            if t[0] == wd:
                return [t[1]]
    for tag in ["P", "A"]:
        if wd in lx.getAll(tag):
            tagOfWord.append(tag)
    if (wd in lx.getAll('N')) or (noun_stem(wd) in lx.getAll('N')):
        if wd in unchanging_plurals_list:
            tagOfWord.append('Np')
            tagOfWord.append('Ns')
        elif noun_stem(wd) == "":
            tagOfWord.append('Ns')
        else:
            tagOfWord.append('Np')
    for tag in ["I","T"]:
        if (wd in lx.getAll(tag)) or (verb_stem(wd) in lx.getAll(tag)) :
            if verb_stem(wd) == "":
                tagOfWord.append(tag + "p")
            else:
                tagOfWord.append(tag + "s")
    return tagOfWord

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.

if __name__ == "__main__":
    print unchanging_plurals_list