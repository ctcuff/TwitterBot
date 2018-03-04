from tweepy import StreamListener


#  Stream used to track the occurrences of a given word
class FilterListener(StreamListener):
    def __init__(self, twitter, keyword, print_status):
        super().__init__()
        self.twitter = twitter
        self.keyword = str(keyword).strip()
        self.word_count = 0
        self.print_status = print_status

    def on_connect(self):
        print("Connection established...")
        print('Listening for occurrences of "' + self.keyword + '"')

    def on_disconnect(self, notice):
        print("Connection dropped: ", notice)

    def on_status(self, status):
        # When a keyword has been detected, update the
        # word count and print out the status
        self.word_count = self.word_count + 1
        print("Occurrences of '" + self.keyword + "': ", self.word_count, sep='')
        if self.print_status is True:
            print("@" + status.author.screen_name)
            print(status.text + "\n")

    def on_error(self, status_code):
        print(status_code)

    def on_exception(self, exception):
        print(exception)
