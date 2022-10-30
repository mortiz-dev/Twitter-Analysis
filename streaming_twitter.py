import tweepy as tw
from datetime import date
import sys
import os
from dotenv import load_dotenv

load_dotenv()

#Claves de acceso
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_secret_token = os.environ.get('ACCESS_SECRET_TOKEN')

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret_token)
api = tw.API(auth)

class CustomStreamListener(tw.Stream):
    def on_status(self, status):
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                print(status.author.screen_name, status.user.location, 'RT', status.created_at, status.retweeted_status.extended_tweet["full_text"], status.retweeted_status.retweet_count)
                print('-----------------')
            except AttributeError:
                print(status.retweeted_status.text)
                print('------------------')
        else:
            try:
                print(status.author.screen_name, 'TW', status.user.location, status.created_at, status.extended_tweet["full_text"])
                print('-----------------')
            except AttributeError:
                print(status.text)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

if __name__ == '__main__':
    streamingAPI = CustomStreamListener(consumer_key, consumer_secret, access_token, access_secret_token)
    streamingAPI.filter(track=['banco nacion', '#banconacion', 'bna+'])