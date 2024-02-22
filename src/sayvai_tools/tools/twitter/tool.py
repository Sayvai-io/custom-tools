class SendTweetMessage:
    def __init__(self, message):
        self.message = message

    def send(self):
        print(f"Sending tweet: {self.message}")