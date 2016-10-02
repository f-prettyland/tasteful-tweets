#!/usr/bin/env python3
import re
import os
import sys
from time import sleep
import random
import string
import argparse
import simplejson
from settings import api
from parser_of_words import loadWords, loadDictionary
from sentiment_score import train_model_and_prepare, score_it

pause_for_effect = 10
threshold = -70

global classifier
classifier = None
bad_nouns = loadWords('dict/bad.noun.txt')
nice_nouns = loadWords('dict/funny.noun.txt')
bad_adjectives = loadWords('dict/bad.adj.txt')
nice_adjectives = loadWords('dict/funny.adj.txt')
dictionary = loadDictionary('dict/dictionary.txt')
b_t_dubs = ["By the way, ", "Oh and "]

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
  worst_score = threshold
  worst_post = None
  for full_status in posts:
    p = full_status['text']
    p_score = score_it(classifier, p)
    # print(p, "\nScore: ", p_score, "\n\n") #debug
    if p_score < worst_score:
      worst_score = p_score
      worst_post = p
  if worst_post:
    status_replace(worst_post)

def status_replace(p):
  print(p)
  edited = happifier(p, nice_nouns, bad_nouns)
  edited = happifier(edited, nice_adjectives, bad_adjectives)
  swapped = []
  for key in  dictionary.keys():
    if key.lower() in edited.lower():
      swapped.append(key)
  if len(swapped) > 0:
    # new_post = api.update_status(status=edited)
    # post_id = new_post['id_str']
    print(edited)
    first = True
    while(len(swapped) > 0):
      sleep(pause_for_effect)
      chosenWord = swapped.pop()
      btw = b_t_dubs[1]
      if first:
        btw = b_t_dubs[0]
        first = False
      defn = btw + chosenWord.lower() + " means " + \
            dictionary[chosenWord.capitalize()].lower()
      print(defn)
      # new_post = api.update_status(status=defn,
                                    # in_reply_to_status_id = post_id)

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
    classifier = train_model_and_prepare()
    main(results)
  except Exception as error:
    print('Caught this error: ' + str(error))
