import sys
sys.path.append('/home/mill/Code/tasteful-tweets')
import json
import argparse
import http_server
import networkx as nx
from settings import api
from networkx.readwrite import json_graph
from sentiment_score import train_model_and_prepare, score_it

MAX_EXPANSIONS = 2
MAX_FOLLOWERS_TO_CHECK = 10
MAX_TWEETS_TO_SCORE = 10

global classifier
classifier = None
global uid_to_user
uid_to_user = {}
uid_to_gid = {}
global gid
gid = 0

class User(object):
  u_id = 0
  screen_name = ""
  avg_score = 0
  interests = []
  follows = []

  def add_friend(fri):
    follows.append(fri)

  def __init__(self, u_id, screen_name, avg_score, interests, follows):
    global gid
    self.u_id = u_id
    uid_to_gid[u_id] = gid
    gid += 1
    self.screen_name = screen_name
    self.avg_score = avg_score
    self.interests = interests
    self.follows = follows


def generate_graph(users):
  G=nx.Graph()
  for user in users:
    G.add_node(uid_to_gid[user.u_id])
    G.node[uid_to_gid[user.u_id]]['score'] = user.avg_score

  for user in users:
    for follow in user.follows:
      # check we've made a node for this person
      if follow in uid_to_gid.keys():
        G.add_edge(uid_to_gid[user.u_id], uid_to_gid[follow])

  # write json formatted data
  d = json_graph.node_link_data(G) # node-link format to serialize
  json.dump(d, open('eye-to-eye/force/force.json','w'))
  print('Wrote node-link JSON data to force/force.json')
  http_server.load_url('eye-to-eye/force/force.html')

def scrape_users(iter_c, users):
  print("iteration ", iter_c)
  print("usser size ", len(users))
  if iter_c >= MAX_EXPANSIONS:
    return []
  nextitr_users = []
  for user in users:
    try:
      followers_response = api.get_followers_ids(user_id=user.u_id,
                                          count=MAX_FOLLOWERS_TO_CHECK)
      for follow_id in followers_response['ids']:
        print(follow_id)
        potential_user = make_user_and_score(follow_id, user.u_id)
        if potential_user:
          nextitr_users.append(potential_user)
    except Exception as error:
      print('Twitter access error for user id: ' + \
        str(user.u_id) + "\n    " + str(error))

  return nextitr_users + scrape_users(iter_c+1, nextitr_users)

def make_user_and_score(usr_id, fri):
  # check not already made
  if usr_id in uid_to_gid.keys():
    uid_to_user[usr_id].add_friend(fri)
    return None
  try:
    usr_deets = api.show_user(user_id = usr_id)
    if fri:
      our_user = User(usr_id, usr_deets['screen_name'], 60, [], [fri])
    else:
      our_user = User(usr_id, usr_deets['screen_name'], -90, [], [])
    uid_to_user[usr_id] = our_user
    return our_user
  except Exception as error:
    print('Twitter access error for user id: ' + \
      str(usr_id) + "\n    " + str(error))
    return None
  # posts = api.get_user_timeline(user_id = usr_id, count = MAX_TWEETS_TO_SCORE)
  # sum_score = 0
  # worst_post = None
  # for full_status in posts:
  #   p = full_status['text']
  #   sum_score += score_it(classifier, p)
  #   print(p, "\nCumul score: ", sum_score, "\n\n") #debug
  # if len(posts) > 0:
  #   usr_deets = api.show_user(user_id = usr_id)
  #   return User(usr_id, usr_deets['screen_name'], sum_score/len(posts), [], [])
  # else:
  #   return None

def main(parsed_args):
  if results.account:
    usr_deets = api.show_user(screen_name = results.account)
    our_users = []
    our_users.append(make_user_and_score(usr_deets['id'], None))
    users_scraped = scrape_users(0, our_users)
    print(len(users_scraped))
    generate_graph(users_scraped)
  else:
    raise Exception('You gotta give me some kinda argument, -h is for help')

if __name__ == "__main__":
  prsr = argparse.ArgumentParser(description='Map some twitter users and ' +\
                                'their posting habits.')

  prsr.add_argument('-a', dest='account',
                      help='A twitter account, addressed by screen name to \
                      evaluate')

  results = prsr.parse_args()
  # test_graph()
  # try:
  classifier
  classifier = train_model_and_prepare()
  main(results)
  # except Exception as error:
  #   print('Caught this error: ' + str(error))
