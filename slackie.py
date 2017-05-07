# Slackie

# Import everything from slackclient as long as other py stuff
from slackclient import *
import os, time, sys, datetime, random

# Read the facts.txt file
with open('facts.txt') as f:
    randomfacts = f.read().splitlines()

# Retrieve global token
token = os.environ.get('SLACK_BOT_TOKEN')

# Bot Functions
def send_message(message, channel):
    sc.api_call("chat.postMessage", channel=channel, text=message, username="Slackie", as_user="Slackie")

# Slack Object
while True:
    sc = SlackClient(token)
    if sc.rtm_connect():
        print('Bot Started !')
        while True:
            try:
                time.sleep(0.1)
                for slack_message in sc.rtm_read():
                    message = slack_message.get("text")
                    user = slack_message.get("user")
                    if message and user:
                        message = message.lower()
                        if message.__contains__("hello") or message.__contains__("hi") or message.__contains__("hey"):
                            send_message("Hello There Human :feet: !", user)

                        elif message == "?" or message == "help":
                            mes = "Options \nHelp - Display Help And Commands \nRandom - Proof That Im Not A Boring Bot :stuck_out_tongue_winking_eye: \n\n"
                            send_message(mes, user)

                        elif message == "whoami":
                            send_message("Your id is : " + user + " :sunglasses:", user)

                        elif message == "random":
                            send_message(random.choice(randomfacts), user)

                        elif message == "why":
                            send_message("Cause i say it! :sunglasses:", user)

                        elif message == "ok":
                            send_message("okay!", user)

                        else:
                            continue
                    else:
                        continue

            except Exception:
                pass
    else:
        print "Connection Failed\nPossible Errors: \n1.Invalid Token\n2.Deactivated Virtual Environment\n3.No Internet Connection"
