#!/usr/bin/env python3
import sys
from functools import reduce
import re
import os
import random
import string
import argparse
import simplejson
from settings import api, __location__


def loadWords(loc):
  try:
    words_file = open(os.path.join(__location__,loc),'r')
    words = [x.strip() for x in words_file.readlines()]
    words_file.close()
    return words
  except IOError:
    raise Exception('Your file %s was not found', loc)

terrible_nouns = loadWords('dict/terrible.txt')
bad_nouns = loadWords('dict/bad.noun.txt')
nice_nouns = loadWords('dict/funny.noun.txt')
bad_adjectives = loadWords('dict/bad.adj.txt')
nice_adjectives = loadWords('dict/funny.adj.txt')

def happifier(replacee, replacers, bad_things):
  regex = re.compile('|'.join(r'(?:\s+|^)'+re.escape(x)+r'(?:\s+|$)'
                      for x in bad_things))
  randomChoice = random.randrange(len(replacers))
  edited = regex.sub(" " + replacers[randomChoice] + " ", replacee)
  new_regex = re.compile('|'.join(r'(?:\s+|^)'+re.escape(x.capitalize())+r'(?:\s+|$)'
                      for x in bad_things))
  randomChoice = random.randrange(len(replacers))
  return new_regex.sub(" " + replacers[randomChoice].capitalize() + " ", edited)

def iterate_timeline(scrn_nam):
  posts = api.get_user_timeline(screen_name = scrn_nam)
  for p in posts:
    status_replace(p)

def status_replace(p):
  print(p['text'])
  edited = happifier(p['text'], nice_nouns, bad_nouns)
  edited = happifier(edited, nice_adjectives, bad_adjectives)
  # api.update_status(status=edited)
  print(edited)


def main(parsed_args):
  if results.tweet_id:
    status_replace(api.lookup_status(id=results.tweet_id)[0])
  elif results.account:
    iterate_timeline(results.account)
  else:
    raise Exception('You gotta give me some kinda argument, -h is for help')

if __name__ == "__main__":
  prsr = argparse.ArgumentParser(description='Create your own better twitter.')

  prsr.add_argument('-t', dest='tweet_id',
                      help='An individual tweet, addressed by ID to change')

  prsr.add_argument('-a', dest='account',
                      help='A twitter account, addressed by screen name to \
                      evaluate')

  # prsr.add_argument('-f', action='store_false', default=False,
  #                     dest='boolean_switch',
  #                     help='Set a switch to false')
  results = prsr.parse_args()
  try:
    main(results)
  except Exception as error:
    print('Caught this error: ' + str(error))
