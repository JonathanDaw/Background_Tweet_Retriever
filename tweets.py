import time
from api_keys import *

recent_tweets = []
want_replies = input('Do you want to see the user\'s own replies?')

def validTweet(tweet):
    if want_replies.lower().startswith('y'):
        if (tweet.text.startswith("RT @")) is False: # Shows user's replies to their own tweets 
            return True
    elif ((tweet.text.startswith("RT @") is False) and (tweet.in_reply_to_status_id is None)): # Don't show user's replies
        return True
try:
    while True:    
        for tweet in tweepy.Cursor(api.user_timeline, id="jacobwolf").items(10):
            if validTweet(tweet):
                if tweet.text not in recent_tweets:
                    print("New Tweet!\n" + tweet.text + "\n")
                    recent_tweets.append(tweet.text)
                    # if (len(recent_tweets) >= 9):
                    #     print("hello")
                    #     print(len(recent_tweets))
                    #     recent_tweets.pop(0)
        time.sleep(3)
except KeyboardInterrupt:
    pass