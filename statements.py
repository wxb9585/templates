# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here
    def __init__(self):
        self.cat = {'P':[],'N':[],'A':[],'T':[],'I':[]}
    def add(self,stem,cat):
        if not cat in self.cat.keys():
            return "It is not the tag we need"
        else:
            self.cat[cat].append(stem)

    def getAll(self, cat):
        a = set(self.cat[cat])
        b = list(a)
        return b


class FactBase:
    """stores unary and binary relational facts"""
    # add code here
    def __init__(self):
        self.unary = {}
        self.binary = {}

    def addUnary(self,pred,e1):
        if not pred in self.unary.keys():
            self.unary[pred] = []

        self.unary[pred].append(e1)

    def addBinary(self,pred,e1,e2):
        if not pred in self.binary.keys():
            self.binary[pred] = []

        self.binary[pred].append((e1,e2))

    def queryUnary(self, pred, e1):
        if pred in self.unary.keys() and e1 in self.unary[pred]:
            return True
        else:
            return False

    def queryBinary(self, pred, e1, e2):
        if (pred in self.binary.keys()) and ((e1,e2) in self.binary[pred]):
            return True
        else:
            return False


import re
from nltk.corpus import brown


def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # add code here
    if re.match(".*[aeiou]ys$",s):
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
    elif s == "has":
        snew = "have"
    elif len(s)>=5 and re.match(".*[^aeiou]ies$",s):
        snew = s[:-3] + 'y'
    elif re.match(".*([ox]|[cs]h|ss|zz)es$",s):
        snew = s[:-2]
    else:
        snew = ""
    if snew != "" and snew != "have":
       if not ( (snew, "VB") in (brown.tagged_words()) and (s, "VBZ") in (brown.tagged_words())):
           snew = ""

    return snew

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg

#if __name__ == "__main__":
    #test = ["eats", "tells","shows","pays","buys","flies","tries","unifies",
    #        "dies","lies","ties","goes","boxes","attaches","washes","dresses",
    #        "fizzes","loses","dazes","lapses","analyses","has","likes","hates","bathes"]
    #for ve in test:
    #    print verb_stem(ve)
    #    print '\n'

# End of PART A.

