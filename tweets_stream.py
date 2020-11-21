import datetime
import json
import sys
import time

from win10toast import ToastNotifier

from api_keys import *


class streamSetup():
    
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth, listener)
    
    @staticmethod
    def getUsersList():
        
        users_list = input('Enter a list of users to track their tweets: ')
        print(users_list.split(","))
        return users_list.split(",")
            
            
    def start(self, users_list=""):
        id_list = []
        for user in users_list:
            id_list.append(api.get_user(user).__dict__['id_str'])
            
        self.stream.filter(id_list, is_async=True)
        
        
class StreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        toaster = ToastNotifier()
        json_load = json.loads(raw_data)
        
        if json_load['in_reply_to_user_id'] is None and 'retweeted_status' not in json_load.keys(): 
            text = json_load['text']
            name = json_load['user']['name']
            # timestamp = json_load['created_at']
            timestamp = datetime.datetime.now()
            print(json.dumps(name))
            print(timestamp)
            # print(json.dumps(timestamp))
            toaster.show_toast("New Tweet", text, icon_path="twitter.ico", duration=3)
            print("New Tweet From\n" + json.dumps(text))
            return True
        
    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.
        
if __name__ == "__main__":
    try:
        streamListener = StreamListener()
        stream = streamSetup(auth, streamListener)
        
        stream.start(streamSetup.getUsersList())
    
    except KeyboardInterrupt:
        sys.exit()
        
