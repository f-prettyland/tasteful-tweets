# ---- Some stream stuff ---- 
# class MyStreamer(TwythonStreamer):
#   def on_success(self, data):
#     if 'text' in data:
#       print (data['text'])
#
# def on_error(self, status_code, data):
#     print (status_code)
#     self.disconnect()
#
# stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET,
#                     ACCESS_KEY, ACCESS_SECRET)
#
# stream.statuses.filter(track='twitter')


def randomTweet():
  try:
    tweetsFile = open(os.path.join(__location__,'tweets.txt'),'r')
    tweetsList = tweetsFile.readlines()
    tweetsFile.close()
    randomChoice = random.randrange(len(tweetsList))
    print (tweetsList[randomChoice]) #For debugging only
    api.update_status(status=tweetsList[randomChoice])
    return None
  except IOError:
    return None

def post(tweet_s):
  api.update_status(tweet_s)

def scrape():
  ids = "782139418517831680"
  users = api.lookup_user(user_id = ids)

  for entry in users:
    r = {}
    r['id'] = entry['id']
    r['screen_name'] = entry['screen_name']
    r['name'] = entry['name']
    r['created_at'] = entry['created_at']
    r['url'] = entry['url']
    r['followers_count'] = entry['followers_count']
    r['friends_count'] = entry['friends_count']
    r['statuses_count'] = entry['statuses_count']
    r['favourites_count'] = entry['favourites_count']
    r['listed_count'] = entry['listed_count']
    r['contributors_enabled'] = entry['contributors_enabled']
    r['description'] = entry['description']
    r['protected'] = entry['protected']
    r['location'] = entry['location']
    r['lang'] = entry['lang']
    if 'url' in entry['entities']:
        r['expanded_url'] = entry['entities']['url']['urls'][0]['expanded_url']
    else:
        r['expanded_url'] = ''
    print(r)
