import os
import sys
import json
from datetime import datetime

import requests
from flask import Flask, request

from parse_message import parse_message

PAGE_ACCESS_TOKEN = os.getenv("EMOJI_ESSAY_BOT_PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("EMOJI_ESSAY_BOT_VERIFY_TOKEN")

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:

            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):

                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]

                    reply = parse_message(message_text)
                    send_message(sender_id, reply)

                # if messaging_event.get("delivery"):
                #     pass

                # if messaging_event.get("optin"):
                #     pass

                # if messaging_event.get("postback"):
                #     pass

    return "ok", 200


def send_message(recipient_id, message_text):
    log("Sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):
    if type(msg) is dict:
        msg = json.dumps(msg)
    else:
        msg = msg.format(*args, **kwargs)
    print("{}: {}".format(datetime.now(), msg))
    sys.stdout.flush()
