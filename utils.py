import random
from time import sleep

import tweepy

from dictionary import quote
from keys import *


def set_up_twitter():  # Initial setup of the Twitter bot
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter = tweepy.API(auth)
    return twitter


def send_direct_message(twitter, user, message):
    twitter.send_direct_message(screen_name=user, text=message)
    try:
        # Handle the user sending a string
        print("Sending: " + message + "\nTo: @" + user)
    except TypeError:
        # Handle the user sending an integer
        print("Sending: ", message, " \nTo: @" + user, sep="")


def follow(twitter, new_follower):
    twitter.create_friendship(new_follower)


def update_status(twitter, message):
    twitter.update_status(message)
    print("Status updated to: " + message)


def tweet_random_quote(twitter, user):  # Enter None as a parameter for user to update the status instead
    number_of_quotes = quote.__len__()
    # Generate a list of random numbers, from 0 to whatever number_of_quotes is
    random_list = random.sample(range(number_of_quotes), number_of_quotes)
    for i in range(number_of_quotes):
        if user is not None:
            twitter.send_direct_message(twitter, user, quote[random_list[i]])
        else:
            # Update the bot's status to a random quote every hour
            twitter.update_status(twitter, quote[random_list[i]])
            sleep(3600)
