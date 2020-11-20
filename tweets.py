import time

import setuptools
from win10toast import ToastNotifier

from api_keys import *


def validTweet(tweet, want_replies):
    """
    validTweet() verifies if the tweet passed in meets the user's criteria. 
                 (whether the user wants to see replies or not)
                 Also filters out retweets from the Twitter User

    Args:
        tweet (Status object): Individual tweet object taken from the overall list of tweets parsed
                               from the desired Twitter Feed. Includes all object information attached 
                               along with the tweet text.
        want_replies (String): User input specifying whether or not to show the Twitter User's
                               replies, or to only display direct tweets from that user.

    Returns:
        Bool: Returns True if the tweet is deemed valid.
              Returns None if the tweet is deemed invalid.
    """
    if want_replies.lower().startswith('y'):
        if (tweet.text.startswith("RT @")) is False: # Shows user's replies to their own tweets 
            return True
    elif ((tweet.text.startswith("RT @") is False) and (tweet.in_reply_to_status_id is None)): # Does not show user's replies
        return True

def main():
    toaster = ToastNotifier()
    recent_tweets = []
    
    want_replies = input('Do you want to see the user\'s own replies?')
    try:
        while True:    
            for tweet in tweepy.Cursor(api.user_timeline, id="jacobwolf").items(10):
                if validTweet(tweet, want_replies):
                    if tweet.text not in recent_tweets:
                        toaster.show_toast("New Tweet", tweet.text, icon_path="twitter.ico", duration=3)
                        print("New Tweet!\n" + tweet.text + "\n")
                        recent_tweets.append(tweet.text)
            time.sleep(5)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
