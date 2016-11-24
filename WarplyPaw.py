# WarplyPaw Version 1.4 (Thursday 24 November 2016)
from slackclient import *
import os, time, sys, datetime, random

with open('facts.txt') as f:
    randomfacts = f.read().splitlines()

# Players
players = {}

# Global Variables
# BOT_ID = os.environ.get("BOT_ID")
token = os.environ.get('SLACK_BOT_TOKEN')

# Bot Functions
def send_message(msg, chnl):
    sc.api_call("chat.postMessage", channel=chnl, text=msg, username="WarplyPaw", as_user="WarplyPaw")

# Customers
clients = ["one", "two", "three"]

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
                            mes = "Options \nHelp - Display Help And Commands \nClients or Customers - Show Active Clients\nRandom - Proof That Im Not A Boring Bot :stuck_out_tongue_winking_eye: \n\n"
                            send_message(mes, user)

                        elif message == "clients" or message == "customers":
                            send_message(str(clients).replace('[', '').replace(']', ''), user)

                        elif message == "whoami":
                            send_message("Your id is : " + user + " :sunglasses:", user)

                        elif message == "enter league":
                            if user in players:
                                send_message("You already have registered!", user)
                            else:
                                players[str(user)] = 0
                                send_message("You just entered Basket League \n your id is : " + user + " :basketball:", user)

                        elif message == "show my stats":
                            if user in players:
                                send_message("Your have : " + str(players[user]) + " Points!  :basketball:", user)
                            else:
                                send_message("You have not participated in League", user)

                        elif message.__contains__("point "):
                            words = message.split(" ")
                            if words[1] == "add":
                                if user in players:
                                    players[user] += 1
                                    send_message("Your score is now : " + str(players[user]), user)
                                else:
                                    send_message("You have not participated in League", user)

                            elif words[1] == "dec":
                                if user in players:
                                    players[user] -= 1
                                    send_message("Your score is now : " + str(players[user]), user)
                                else:
                                    send_message("You have not participated in League", user)
                            else:
                                continue

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