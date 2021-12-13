import tweepy
from kafka import KafkaProducer
import json

consumer_key=""
consumer_key_secret=""
access_token=""
access_token_secret=""

auth=tweepy.OAuthHandler(consumer_key,consumer_key_secret)
auth.set_access_token(access_token,access_token_secret)
producer = KafkaProducer(bootstrap_servers='master:9092')

topic_name = "test2"

class MyListener(tweepy.Stream):
    def on_data(self, data):
      json_ = json.loads(data)
      if "lang" in json_:
        producer.send(topic_name, json_["lang"].encode('utf8'))
        print(json_["lang"])
      return True
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = MyListener(
  consumer_key, consumer_key_secret,
  access_token, access_token_secret
)
twitter_stream.filter(track='#movie')