#!/usr/bin/env python3
import sys
from functools import reduce
import re
import string
#import simplejson
import os
import random
#from settings import api, __location__

bad_nouns = []
nice_nouns = []
bad_adjectives = []
nice_adjectives = []
current_dictionary_word=""
toReplace=False
dictionary={"key":"value", "mike":"drunk"}

def happifier(replacee, lookup, replacers):
  global toReplace
  toReplace=False
  for x in lookup:
    if x in replacee.lower():
      toReplace=True

  if(toReplace==False):
    return replacee

  else:
    regex = re.compile('|'.join(r'(?:\s+|^)'+re.escape(x)+r'(?:\s+|$)'
                      for x in lookup))
    randomChoice = random.randrange(len(replacers))
    global chosenWord
    chosenWord=replacers[randomChoice]
    return regex.sub(" " + chosenWord + " ", replacee.lower())

def status_replace():

  posts = ["Crooked Hillary - - Makes History!", 
           "They should be forced to suffer and, when they kill, they should be executed for their crimes"]
  for p in posts:
    print (p)
    print(happifier(p, bad_adjs, funny_adjs))
    if(toReplace == False):
      print(happifier(p, bad_nouns,funny_nouns))
    print(toReplace)   
    
    if (toReplace == True):
      print (chosenWord + " is the word being replaced.")
      if chosenWord.capitalize() in dictionary.keys():
        return "By the way, " + chosenWord + " just means " + dictionary[chosenWord.capitalize()]
        
    

def loadWords(loc):
  try:
    words_file = open("/Users/developer/Desktop/projects/peaceHackathon/tasteful-tweets/"+loc,'r')
    words = [x.strip().lower() for x in words_file.readlines()]
    words_file.close()
    return words 
  except IOError:
    return {}


def loadDictionary(loc):
  try:
    global dictionary
    words_file = open("/Users/developer/Desktop/projects/peaceHackathon/tasteful-tweets/"+loc,'r')
    for x in words_file:
      key = x.split(',')[0] 
      value = x.split(',')[1]
      #print (key, value)
      dictionary[key] = value

    words_file.close() 
    #print dictionary
  except IOError:
    return {}

bad_adjs = loadWords('dict/bad.adj.txt')

funny_adjs = loadWords('dict/funny.adj.txt')

bad_nouns = loadWords('dict/bad.noun.txt')

funny_nouns = loadWords('dict/funny.noun.txt')

loadDictionary('dict/dictionary.txt')

print ( dictionary)

print(status_replace())
