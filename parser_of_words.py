#!/usr/bin/env python3
import os
import string
from settings import __location__

def loadDictionary(loc):
  try:
    dictionary = {}
    words_file = open(loc)
    for x in words_file:
      key = x.split(',')[0]
      value = x.split(',')[1]
      dictionary[key] = value
    words_file.close()
    return dictionary
  except IOError:
    return {}

def loadWords(loc):
  try:
    words_file = open(os.path.join(__location__,loc),'r')
    words = [x.strip() for x in words_file.readlines()]
    words_file.close()
    return words
  except IOError:
    raise Exception('Your file %s was not found', loc)
