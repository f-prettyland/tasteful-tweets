#!/usr/bin/env python3
import sys
from functools import reduce
import re
import string
import simplejson
import os
import random
from settings import api, __location__

bad_nouns = {}
nice_nouns = {}
bad_adjectives = {}
nice_adjectives = {}

def happifier(replacee, replacers):
  regex = re.compile('|'.join(r'(?:\s+|^)'+re.escape(x)+r'(?:\s+|$)'
                      for x in bad_nouns))
  randomChoice = random.randrange(len(replacers))
  return regex.sub(" " + replacers[randomChoice] + " ", replacee)

def status_replace():
  posts = api.get_user_timeline(screen_name = "HateToHearts")
  for p in posts:
    print(p['text'])
    print(happifier(p['text'], nice_nouns))

def loadWords(loc):
  try:
    words_file = open(os.path.join(__location__,loc),'r')
    words = [x.strip() for x in words_file.readlines()]
    words_file.close()
    return words
  except IOError:
    return {}

bad_nouns = loadWords('dict/bad.txt')
nice_nouns = loadWords('dict/good.txt')

status_replace()
