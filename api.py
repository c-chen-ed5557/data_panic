import requests
import random
# import spotipy
# import spotipy.util as util
import ast
from twython import Twython
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
    data = {
            'title': news['title'],
            'author': news['author'],
            'content': parse_news_content(news['content'])
           }
    return data

# The requested news contents contain some Unicode or Latin1 characters.
# They need to be cleaned via this function.
def parse_news_content(string):
    string = string.encode('ascii', 'ignore').decode('ascii')
    return string

# This is to request a random quote via quotes api.
def request_quotes():
    url = "https://yusufnb-quotes-v1.p.rapidapi.com/widget/~einstein.json"

    headers = {
        'x-rapidapi-host': "yusufnb-quotes-v1.p.rapidapi.com",
        'x-rapidapi-key': "e77e401534msha5ef44aa585ba64p17a067jsne00d370ea234"
    }
    response = requests.request("GET", url, headers=headers)
    data = parse_quotes(response.text)
    return data

# The quotes requested are strings which represent dicts.
# They need to be turned into dicts with this function.
# User ast module from Python 2.6
def parse_quotes(string):
    parsed_dict = ast.literal_eval(string)
    return parsed_dict

# This is to request a tweet message from Twitter api.
def request_tweets(q_list=['python', 'rock', 'food', 'joker']):
    # topics = ['']
    twitter = Twython(consumer_key,
                      consumer_secret,
                      access_token,
                      access_token_secret)
    keyword = q_list[int(random.random()*len(q_list))]
    results_generator = twitter.cursor(twitter.search, q=keyword)
    result = next(results_generator)

    data = {
        'username': result['user']['name'],
        'content': result['text'],
        'keyword': keyword
    }

    return data

def parse_tweets_content():
    pass

# def request_videos():

# def request_music():


# def request_music():
#     sp = spotipy.Spotify()
#     token = util.prompt_for_user_token(client_id, client_secret)
    # if token:
        # sp.recommendations(auth=token)
