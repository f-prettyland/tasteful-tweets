#!/usr/bin/env python3
import sys
from functools import reduce
import re
import string
import simplejson
import os
import random
from settings import api, __location__

terrible_nouns = {}
bad_nouns = {}
nice_nouns = {}
bad_adjectives = {}
nice_adjectives = {}

def happifier(replacee, replacers, bad_things):
  regex = re.compile('|'.join(r'(?:\s+|^)'+re.escape(x)+r'(?:\s+|$)'
                      for x in bad_things))
  randomChoice = random.randrange(len(replacers))
  return regex.sub(" " + replacers[randomChoice] + " ", replacee.lower())

def iterate_timeline(scrn_nam):
  posts = api.get_user_timeline(screen_name = scrn_nam)
  for p in posts:
    status_replace(p)

def status_replace(p):
  print(p['text'])
  edited = happifier(p['text'], nice_nouns, bad_nouns)
  edited = happifier(edited, nice_adjectives, bad_adjectives)
  print(edited)

def loadWords(loc):
  try:
    words_file = open(os.path.join(__location__,loc),'r')
    words = [x.strip() for x in words_file.readlines()]
    words_file.close()
    return words
  except IOError:
    return {}

terrible_nouns = loadWords('dict/terrible.txt')
bad_nouns = loadWords('dict/bad.txt')
nice_nouns = loadWords('dict/good.txt')
bad_adjectives = loadWords('dict/bad.adj.txt')
nice_adjectives = loadWords('dict/funny.adj.txt')

iterate_timeline("HateToHearts")
