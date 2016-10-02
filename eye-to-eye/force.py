import sys
sys.path.append('/home/mill/Code/tasteful-tweets')
import json
import argparse
import http_server
import networkx as nx
from settings import api
from networkx.readwrite import json_graph
from sentiment_score import train_model_and_prepare, score_it

max_expansions = 1
max_followers_to_check = 200

global classifier
classifier = None

class User(object):
  u_id = 0
  screen_name = ""
  avg_score = 0
  interests = []
  follows = []

  def __init__(self, u_id, screen_name, avg_score, interests, follows):
    self.u_id = u_id
    self.screen_name = screen_name
    self.avg_score = avg_score
    self.interests = interests
    self.follows = follows

def generate_graph(users):
  G=nx.Graph()
  for user in users:
    G.add_node(user.u_id)
    G.node[user.u_id]['score'] = user.avg_score

  for user in users:
    for follow in user.follows:
      G.add_edge(user.u_id, follow)

  # write json formatted data
  d = json_graph.node_link_data(G) # node-link format to serialize
  json.dump(d, open('eye-to-eye/force/force.json','w'))
  print('Wrote node-link JSON data to force/force.json')
  # open URL in running web browser
  http_server.load_url('eye-to-eye/force/force.html')
  print('Or copy all files in force/ to webserver and load force/force.html')

def scrape_users(iter_c, users):
  if iter_c >= max_expansions:
    return users
  for user in users:
    follow_ids = api.get_followers_ids(user_id=user.u_id, count=max_followers_to_check)
    print(follow_ids)

def iterate_timeline(usr_id):
  usr_deets = api.show_user(user_id = usr_id)
  return User(usr_id, usr_deets['screen_name'], 20, [], [])
  # posts = api.get_user_timeline(user_id = usr_id)
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
    our_users.append(iterate_timeline(usr_deets['id']))
    scrape_users(0, our_users)
  else:
    raise Exception('You gotta give me some kinda argument, -h is for help')

if __name__ == "__main__":
  prsr = argparse.ArgumentParser(description='Map some twitter users and ' +\
                                'their posting habits.')

  prsr.add_argument('-a', dest='account',
                      help='A twitter account, addressed by screen name to \
                      evaluate')

  results = prsr.parse_args()
  # try:
  classifier
  classifier = train_model_and_prepare()
  main(results)
  # except Exception as error:
  #   print('Caught this error: ' + str(error))
