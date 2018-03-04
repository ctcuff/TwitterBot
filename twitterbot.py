import tweepy

import utils
from filterlistener import FilterListener
from userlistener import UserListener

twitter = utils.set_up_twitter()
print("Would you like to start the user stream [1] or the filter stream [2] ", end="")
while True:
    try:
        mode = int(input())
        if mode == 1:
            stream = tweepy.Stream(auth=twitter.auth, listener=UserListener(twitter))
            stream.userstream()
            break
        elif mode == 2:
            keyword = input("Enter the filter word: ")
            stream = tweepy.Stream(auth=twitter.auth, listener=FilterListener(twitter, keyword, True))
            stream.filter(track=[keyword])
            break
        else:
            print("Please enter [1] or [2] ", end="")
            continue
    except ValueError:
        print("Please enter [1] or [2] ", end="")
        continue
