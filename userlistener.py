import json
import random
from time import sleep

from tweepy import StreamListener

import utils
from dictionary import *


# Stream used to reply to messages, update status, etc...
class UserListener(StreamListener):
    def __init__(self, twitter):
        super().__init__()
        self.twitter = twitter

    def on_connect(self):
        print("Connection established... listening for messages")

    def on_disconnect(self, notice):
        print("Connection dropped... ", notice)

    def on_data(self, raw_data):
        # tweepy doesn't format the JSON so we need to do it here
        json_data = str(raw_data)
        json_formatted_string = json_data.replace("\\", "")
        json_data = json.loads(json_formatted_string)

        num_quotes = quote.__len__() - 1
        num_misunderstandings = misunderstandings.__len__() - 1
        num_bot_greetings = bot_greetings.__len__() - 1

        if 'direct_message' in json_data.keys():
            message = json_data['direct_message']['text']
            sender = json_data['direct_message']['sender_screen_name']
            message = str(message).lower().strip()

            wants_quote = message.__contains__('quote')
            was_greeting = message in user_greetings
            was_google_search = message.startswith("search google for")
            was_question = message.endswith("?")
            wants_joke = message.__contains__("joke")

            # Since on_data is triggered when sending AND receiving a message,
            # we need to check who sends the message. This way, the bot doesn't
            # reply to itself or send duplicate messages
            if not sender == "CamsTweetBot":
                print("Message from @" + sender)
                print(message)

                if wants_quote:
                    random_index = random.randint(0, num_quotes)
                    utils.send_direct_message(self.twitter, sender, quote[random_index])

                elif was_greeting:
                    random_index = random.randint(0, num_bot_greetings)
                    utils.send_direct_message(self.twitter, sender, bot_greetings[random_index])

                elif was_google_search:
                    # The user searched for one word so we extract that one word
                    search_query = message.replace(" ", "+")
                    if search_query.__len__() == 4:
                        utils.send_direct_message(
                            self.twitter, sender, "Here yo go:\nhttps://www.google.com/search?q=" + search_query[3])
                    else:
                        # The user searched for multiple words so we extract the words after 'for'
                        multi_search_query = message.replace("search google for ", "").replace(" ", "+")
                        utils.send_direct_message(
                            self.twitter, sender, "Here you go:\nhttps://www.google.com/search?q=" + multi_search_query)

                elif was_question:
                    greet_check = message.rstrip("?")
                    if greet_check in user_greetings:
                        random_index = random.randint(0, num_bot_greetings)
                        utils.send_direct_message(self.twitter, sender, bot_greetings[random_index])
                    else:
                        search_query = message.replace("?", "").strip().replace(" ", "+")
                        utils.send_direct_message(
                            self.twitter, sender, "This might help:\nhttps://www.google.com/search?q=" + search_query)

                elif wants_joke:
                    utils.send_direct_message(self.twitter, sender, "Sorry, I don't know any good jokes yet!")

                else:
                    random_index = random.randint(0, num_misunderstandings)
                    utils.send_direct_message(self.twitter, sender, misunderstandings[random_index])

        elif 'event' and 'source' and 'target' in json_data.keys():
            new_follower = json_data['source']['screen_name']
            # make sure the bot doesn't follow itself
            if not new_follower == "CamsTweetBot":
                print("@" + new_follower + " followed you")
                random_index = random.randint(0, num_quotes)
                utils.follow(self.twitter, new_follower)
                utils.send_direct_message(self.twitter, new_follower, "Thanks for following, here's a quote")
                sleep(1)
                utils.send_direct_message(self.twitter, new_follower, quote[random_index])

    def on_exception(self, exception):
        print(str(exception))

    def on_error(self, status_code):
        print(str(status_code))
