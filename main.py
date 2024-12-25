import tracemalloc

tracemalloc.start()

import asyncio
from twikit import Client
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint


MINIMUM_TWEETS = 100
QUERY = 'bitcoin'

config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

# creating csv file



async def main():
    client=Client(language='en-US')
    # await client.login(auth_info_1=username, auth_info_2=email, password=password)
    # client.login(auth_info_1=username, auth_info_2=email, password=password)
    # client.save_cookies('cookies.json')
    client.load_cookies('cookies.json')
    with open('tweets.csv', mode='w', newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['S.No', 'User', 'Tweet', 'Date', 'Retweets', 'Likes'])
    tweet_count=0
    tweets=None
    while tweet_count<MINIMUM_TWEETS:
        if tweets is None:
            print(f'{datetime.now()}- Getting tweets... ')
            tweets=await client.search_tweet(QUERY, product='Latest')
        else:
            wait_time=randint(5,10)
            print(f'{datetime.now()}- Getting next tweets after {wait_time} seconds... ')
            time.sleep(wait_time)
            tweets=await tweets.next()
        for tweet in tweets:
            tweet_count+=1
            tweet_data=[tweet_count,tweet.user.name,tweet.text,tweet.created_at,tweet.retweet_count,tweet.favorite_count]
            with open('tweets.csv', mode='a', newline='',encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data) 
    print(f"Total tweets: {tweet_count}")

asyncio.run(main())