import json
import sys
import time

from win10toast import ToastNotifier

from api_keys import *


class streamSetup():
    
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)
    
    def start(self, users=""):
        users_list = []
        for user in users:
            users_list.append(api.get_user(user).__dict__['id_str'])
            
        self.stream.filter(users_list)
        
        
class StreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        toaster = ToastNotifier()
        json_load = json.loads(raw_data)
        
        if json_load['in_reply_to_user_id'] is None and 'retweeted_status' not in json_load.keys(): 
            text = json_load['text']
            toaster.show_toast("New Tweet", text, icon_path="twitter.ico", duration=3)
            print("New Tweet!\n" + json.dumps(text))
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
        stream.start(["every3minutes", "jacobwolf"])
    
    except KeyboardInterrupt:
        sys.exit()
        
