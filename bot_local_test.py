#!/usr/bin/env python3
import sys
from functools import reduce
import re
import string
#import simplejson
import os
import random
#from settings import api, __location__

bad_nouns = {}
nice_nouns = {}
bad_adjectives = {}
nice_adjectives = {}

def happifier(replacee, lookup, replacers):
  regex = re.compile('|'.join(r'(?:\s+|^)'+re.escape(x)+r'(?:\s+|$)'
                      for x in lookup))
  randomChoice = random.randrange(len(replacers))
  return regex.sub(" " + replacers[randomChoice] + " ", replacee.lower())

def status_replace():
  posts = ["Crooked Hillary - - Makes History!", 
           "They should be forced to suffer and, when they kill, they should be executed for their crimes"]
  for p in posts:
    print (p)
    #print(happifier(p, bad_adjs, funny_adjs))
    print(happifier(p, bad_nouns,funny_nouns))

def loadWords(loc):
  try:
    words_file = open("/Users/developer/Desktop/projects/peaceHackathon/tasteful-tweets/"+loc,'r')
    words = [x.strip().lower() for x in words_file.readlines()]
    words_file.close()
    return words
  except IOError:
    return {}


bad_adjs = loadWords('dict/bad.adj.txt')

funny_adjs = loadWords('dict/funny.adj.txt')

bad_nouns = loadWords('dict/bad.noun.txt')

funny_nouns = loadWords('dict/funny.noun.txt')

print (bad_nouns, funny_nouns)

status_replace()
