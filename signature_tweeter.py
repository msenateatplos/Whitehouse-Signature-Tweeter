#!/usr/bin/python

from time import gmtime, strftime, strptime
import sys
#import requests
#import json
#from bs4 import BeautifulSoup
from config import *
import os
import Queue
import logging
from parser import *
from tweeter import *

class mutable_int:
    def __init__(self):
        self.value = 0;
    def set(self, value):
        self.value = value
    def get(self):
        return self.value

#open db connection
#import sqlite3
#conn = sqlite3.connect(database) # db defined in config.py
#c = conn.cursor()

#start logger
logger = logging.getLogger('main')

twitter_Queue = Queue.Queue(10000)
exit_event = threading.Event()
signature_count = mutable_int()

parser_thread = parser("parser", 20, wh_url_base, wh_url_id1, wh_url_id2, 
                       twitter_Queue, signature_count, exit_event, database)
tweetbot = Tweeter(consumer_key, consumer_secret, access_token, access_token_secret, 
                   msg_preamble, msg_postamble, twitter_Queue, signature_count, 
                   exit_event, 10, twitter_live_mode)

parser_thread.start()
tweetbot.start()

raw_input("Press enter to end . . .")
exit_event.set()
print "exiting . . ."

parser_thread.join()
tweetbot.join()

logger.info('exiting thread')
print "Exiting: main thread"

######################## EXTRA INFO #########################

# Sample of format of signatures from http request response
'''
<div class="name">Robert G</div><!--/name-->
<div class="details">
Los Angeles, CA<br/>
May 23, 2012<br/>
Signature # 13,711    </div>
</div>, <div class="entry entry-reg ">
<div class="name">Trystan G</div><!--/name-->
<div class="details">
<br/>
May 23, 2012<br/>
Signature # 13,710    </div>
</div>, <div class="entry entry-reg ">
<div class="name">Vinay S</div><!--/name-->
<div class="details">
Carmel, IN<br/>
May 23, 2012<br/>
Signature # 13,709    </div>
</div>
'''
