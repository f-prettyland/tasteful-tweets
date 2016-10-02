import sys
sys.path.append('/home/mill/Code/tasteful-tweets')
import json
import argparse
import http_server
import networkx as nx
from settings import api
from networkx.readwrite import json_graph
from sentiment_score import train_model_and_prepare, score_it

global classifier
classifier = None

class User(object):
  screen_name = ""
  avg_score = 0
  interests = []
  follows = []

  def __init__(self, screen_name, avg_score, interests, follows):
    self.screen_name = screen_name
    self.avg_score = avg_score
    self.interests = interests
    self.follows = follows

def generate_graph():
  G=nx.Graph()
  G.add_node(1)
  G.add_nodes_from([2,3])

  G.node[1]['score'] = 1
  G.node[2]['score'] = 2
  G.node[3]['score'] = 15

  for n in G:
      G.node[n]['name'] = n

  # write json formatted data
  d = json_graph.node_link_data(G) # node-link format to serialize
  json.dump(d, open('eye-to-eye/force/force.json','w'))
  print('Wrote node-link JSON data to force/force.json')
  # open URL in running web browser
  http_server.load_url('eye-to-eye/force/force.html')
  print('Or copy all files in force/ to webserver and load force/force.html')

def iterate_timeline(scrn_nam):
  posts = api.get_user_timeline(screen_name = scrn_nam)
  sum_score = threshold
  worst_post = None
  for full_status in posts:
    sum_score += score_it(classifier, p)
    # print(p, "\nScore: ", p_score, "\n\n") #debug
  if len(posts) > 0:
    user = User(scrn_nam, sum_score/len(posts), [])

def main(parsed_args):
  generate_graph()
  # if results.account:
  #   iterate_timeline(results.account)
  # else:
  #   raise Exception('You gotta give me some kinda argument, -h is for help')

if __name__ == "__main__":
  prsr = argparse.ArgumentParser(description='Map some twitter users and ' +\
                                'their posting habits.')

  prsr.add_argument('-a', dest='account',
                      help='A twitter account, addressed by screen name to \
                      evaluate')

  results = prsr.parse_args()
  try:
    classifier
    classifier = train_model_and_prepare()
    main(results)
  except Exception as error:
    print('Caught this error: ' + str(error))
