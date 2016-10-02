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

global debug_mode
global score_it_mode
global tweet_back_mode
global classifier
classifier = None
bad_nouns = loadWords('dict/bad.noun.txt')
nice_nouns = loadWords('dict/funny.noun.txt')
bad_adjectives = loadWords('dict/bad.adj.txt')
nice_adjectives = loadWords('dict/funny.adj.txt')
dictionary = loadDictionary('dict/dictionary.txt')
b_t_dubs = ["By the way, ", "Oh and "]


def happifier(replacee, replacers, bad_things):
  regex = re.compile('|'.join(r'(?:|^)'+re.escape(x)+r'(?:|$)'
                      for x in bad_things))
  randomChoice = random.randrange(len(replacers))
  edited = regex.sub( replacers[randomChoice], replacee)
  new_regex = re.compile('|'.join(r'(?:|^)'+re.escape(x.capitalize())+r'(?:|$)'
                      for x in bad_things))
  newRandomChoice = random.randrange(len(replacers))
  return new_regex.sub(replacers[newRandomChoice].capitalize(), edited)


def iterate_timeline(scrn_nam):
  posts = api.get_user_timeline(screen_name = scrn_nam)
  worst_score = threshold
  worst_post = None
  worst_post_id = None
  for full_status in posts:
    p = full_status['text']

    p_score = score_it(classifier, p)
     #print(p, "\nScore: ", p_score, "\n\n") #debug
    if p_score < worst_score:
      worst_score = p_score
      worst_post = p
      worst_post_id = full_status['id']
  if worst_post:
    status_replace(worst_post, scrn_nam, worst_post_id)

def status_replace(p, scrn_nam, twt_id):

  p_score = score_it(classifier, p)

  my_msg="The sentiment anaylsis scoring for this statement being offensive and hateful is: " + str(p_score)

  if score_it_mode:
    print(my_msg)
  else:
    api.update_status(status=my_msg)


  edited = happifier(p, nice_nouns, bad_nouns)
  edited = happifier(edited, nice_adjectives, bad_adjectives)
  swapped = []
  for key in  dictionary.keys():
    if key.lower() in edited.lower():
      swapped.append(key)
  if len(swapped) > 0:
    post_id = -1

    if debug_mode:
      print(edited)
    else:
      new_post = {}
      if tweet_back_mode:
        edited = "@"+scrn_nam+" "+edited
        new_post = api.update_status(status=edited,
                            in_reply_to_status_id = twt_id)
      else:
        new_post = api.update_status(status=edited)
      post_id = new_post['id_str']

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
      if debug_mode:
        print(defn)
      else:
        api.update_status(status=defn,
                                    in_reply_to_status_id = post_id)
  else:
    print("Nothing to swap in here")

def main(parsed_args):
  if results.tweet_id:
    the_tweet = api.lookup_status(id=results.tweet_id)[0]
    status_replace(the_tweet['text'], the_tweet['user']['screen_name'],
                  the_tweet['id'])
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

  prsr.add_argument('-d', dest='debug_mode', action='store_true',
                      help='Just print don\'t tweet')

  prsr.add_argument('-s', dest='score_it', action='store_true',
                     help="Print out the offensive score")

  prsr.add_argument('-r', dest='tweet_back', action='store_true',
                     help="Tweet the result back at them")


  prsr.set_defaults(debug_mode=False)
  prsr.set_defaults(score_it=False)
  prsr.set_defaults(tweet_back=False)

  results = prsr.parse_args()
  debug_mode = results.debug_mode
  score_it_mode = results.score_it
  tweet_back_mode = results.tweet_back
  # try:
  classifier = train_model_and_prepare()
  main(results)
  # except Exception as error:
  #   print('Caught this error: ' + str(error))
