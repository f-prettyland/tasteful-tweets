#!/usr/bin/env python3
import os
from twython import Twython, TwythonStreamer
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

CONSUMER_KEY = 'SECRET-KEY'
CONSUMER_SECRET = 'SECRET-KEY'
ACCESS_KEY = 'SECRET-KEY'
ACCESS_SECRET = 'SECRET-KEY'

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
