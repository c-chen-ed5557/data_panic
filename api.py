import requests
import random
import spotipy
import spotipy.util as util
from twython import Twython
from InstagramAPI import InstagramAPI
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    client_id,
    client_secret
)

# function 'call_api' returns a random result from a certain
# type of medium according to user's choice
def call_api(medium_choice):

    if medium_choice == 'text':
        pass
    elif medium_choice == 'image':
        pass
    elif medium_choice == 'sound':
        pass
    else:
        pass

# This is to request a piece of news from newsapi.org.
def request_news():
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=gb&'
       'apiKey=57f93d392c59452fa5341a4dc1d1c29d')
    response = requests.get(url)
    output = response.json()['articles']
    news = output[int(random.random() * len(output))]

# This is to request a random quote via quotes api.
def request_quotes():
    url = "https://yusufnb-quotes-v1.p.rapidapi.com/widget/~einstein.json"

    headers = {
        'x-rapidapi-host': "yusufnb-quotes-v1.p.rapidapi.com",
        'x-rapidapi-key': "e77e401534msha5ef44aa585ba64p17a067jsne00d370ea234"
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text['quote'])

# This is to request a tweet message from Twitter api.
def request_tweets():
    # topics = ['']
    twitter = Twython(consumer_key,
                      consumer_secret,
                      access_token,
                      access_token_secret)
    q_list = ['python', 'rock', 'food', 'joker']
    results = twitter.cursor(twitter.search, q=int(random.random()*len(q_list)))
    print(next(results)['text'])
    return next(results)['text']

# def request_videos():

# def request_music():


def request_music():
    sp = spotipy.Spotify()
    token = util.prompt_for_user_token(client_id, client_secret)
    # if token:
        # sp.recommendations(auth=token)
