#!/usr/bin/env python3
import sys
from functools import reduce
import re
import string
import simplejson
import os
import random
from settings import api, __location__

bad_words ={}
nice_words ={}

def happifier(to_find, replacee):
  regex = re.compile('|'.join(r'(?:\s+|^)'+re.escape(x)+r'(?:\s+|$)' for x in to_find))
  return regex.sub("",replacee)

def status_replace():
  posts = api.get_user_timeline(screen_name = "HateToHearts")
  try:
    bad_words_file = open(os.path.join(__location__,'dict/bad.txt'),'r')
    bad_words = [x.strip() for x in bad_words_file.readlines()]
    bad_words_file.close()

    for p in posts:
      print(p['text'])
      print(happifier(bad_words, p['text']))
    return None
  except IOError:
    return None

status_replace()
