"""Logic for Emoji Essay Bot Flask app."""

import os
import sys
import json
from datetime import datetime

import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

PAGE_ACCESS_TOKEN = os.getenv("EMOJI_ESSAY_BOT_PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("EMOJI_ESSAY_BOT_VERIFY_TOKEN")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("EMOJI_ESSAY_BOT_DB_URL")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Emoji, FBMessengerMessage
from parse_message import parse_message


@app.route('/', methods=['GET'])
def verify():
    """Verify the Facebook hub challenge."""

    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    """Receive and process Facebook's request."""

    data = request.get_json()
    log(data)

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    # recipient_id = messaging_event["recipient"]["id"]
                    message_mid = messaging_event["message"]["mid"]
                    message_text = messaging_event["message"]["text"]

                    # This is to de-duplicate responses to Facebook.
                    if is_duplicate(message_mid):
                        # HTTP 204 is for "No Content"
                        return "", 204
                    else:
                        add_message_mid(message_mid)

                        reply = parse_message(message_text)
                        send_message(sender_id, reply)

    return "OK", 200


def is_duplicate(message_mid):
    """Query the database for the mid and return True if it exists."""

    r = db.session.query(FBMessengerMessage).filter(  # pylint:disable=no-member
        FBMessengerMessage.message_mid == message_mid)
    r_exists = db.session.query(  # pylint:disable=no-member
        r.exists()).scalar()
    return r_exists


def add_message_mid(message_mid):
    """Add the mid to the database."""

    r = FBMessengerMessage(message_mid=message_mid)
    db.session.add(r)  # pylint:disable=no-member
    db.session.commit()  # pylint:disable=no-member


def send_message(recipient_id, message_text):
    """Log the message and send."""

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
    """Log data to Heroku."""

    if type(msg) is dict:
        msg = json.dumps(msg)
    else:
        msg = msg.format(*args, **kwargs)
    print("{}: {}".format(datetime.now(), msg))
    sys.stdout.flush()
