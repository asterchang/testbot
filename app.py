import os, sys

from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

app = Flask(__name__)

#Assign token information, such as Facebook Fan Club, Messenger APP, Wit
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
FB_BOT_TOKEN = os.environ["FB_BOT_TOKEN"]


bot = Bot(PAGE_ACCESS_TOKEN)

#Create endpoint /testbot response to process FB webhook authentication and verification (GET method )
@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == FB_BOT_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    #Response to normal browser request
    return "Hi CH100 FB Chat Bot testbot API is alive", 200

#Create endpoint /testbot response to process FB webhook message and send back response (POST method)
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    #debug: print out JSON from FB webhook
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    response = None

                    entity, value = wit_response(messaging_text)
                    log(entity)
                    log(value)

                    if entity == 'newstype':
                        response = "Ok, I will send you the {} news".format(str(value))
                    elif entity == 'location':
                        response = "Ok, so you live in {0}. Here are top headlines from {0}".format(str(value))
                    elif entity == '':


                    if response == None:
                        response = "I have no idea what you are saying!"

                    bot.send_text_message(sender_id, response)

    return "Process completed.", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run()
