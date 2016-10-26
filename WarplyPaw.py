# WarplyPaw Version 1.1 (Wednesday 26 October 2016)
# Author Dimitris Filippou

from slackclient import *
import sqlite3
import os
import time
import sys
import random

randomfacts = [
    "Banging your head against a wall burns 150 calories an hour.",
    "Pteronophobia is the fear of being tickled by feathers!",
    "When hippos are upset, their sweat turns red.",
    "The average woman uses her height in lipstick every 5 years.",
    "If you lift a kangaroo's tail off the ground it can't hop.",
    "Bikinis and tampons invented by men.",
    "If you consistently fart for 6 years & 9 months, enough gas is produced to create the energy of an atomic bomb!",
    "You cannot snore and dream at the same time.",
    "Recycling one glass jar saves enough energy to watch TV for 3 hours.",
    "About 8,000 Americans are injured by musical instruments each year.",
    "A small child could swim through the veins of a blue whale.",
    "Hewlett-Packard's name was decided in a coin toss.",
    "The toothpaste 'Colgate' in Spanish translates to 'go hang yourself'.",
    "China has more English speakers than the United States."
    "The longest time between two twins being born is 87 days."
    "n 2007, an American man named Corey Taylor tried to fake his own death in order to get out of his cell phone contract without paying a fee. It didn't work."
    "Everyone has a unique tongue print, just like fingerprints."
    "Most Muppets are left-handed. (Because most Muppeteers are right-handed, so they operate the head with their favoured hand.)"
    "Female kangaroos have three vaginas."
    "In 1567, the man said to have the longest beard in the world died after he tripped over his beard running away from a fire."
    "The top of the Eiffel Tower leans away from the sun, as the metal facing the sun heats up and expands. It can move as much as 7 inches."
    "There are around 60,000 miles of blood vessels in the human body. If you took them all out and laid them end to end, they'd stretch around the world more than twice. But, seriously, don't do that either."
    "95% of people text things they could never say in person"
]

# Global Variables
# BOT_ID = os.environ.get("BOT_ID")
token = os.environ.get('SLACK_BOT_TOKEN')
admin = " "

# Create SQLite Database
cn = sqlite3.connect('WarplyDatabase.db')
print('Database Is Running!')

# Create SQLite Cursor
cur = cn.cursor()

# Create Table For Tasks
try:
    cur.execute('''CREATE TABLE tasks(id INTEGER PRIMARY KEY, username TEXT, client TEXT, activity TEXT, department TEXT, usr_message TEXT, time_worked)''')
    print("Table Has Been Created!")
except sqlite3.OperationalError:
    print("Table Is Already Created!")


# Bot Functions
def send_message(msg, chnl):
    sc.api_call("chat.postMessage", channel=chnl, text=msg, username="WarplyPaw", as_user="WarplyPaw")

# You can change this
clients = ["client1", "client2", "client3"]
activities = ["development", "testing", "designing"]
departments = ["delivery", "marketing", "design"]

# Slack Object
sc = SlackClient(token)

# Check Web Socket Connection
if sc.rtm_connect():
    print('Bot Started !')
    while True:
        for slack_message in sc.rtm_read():
            message = slack_message.get("text")
            user = slack_message.get("user")
            if not message or not user:
                continue
            
            # Message Control
            message = message.lower()
            
            if message.__contains__("hello") or message.__contains__("hi") or message.__contains__("hey"):
                send_message("Hello There Human :slightly_smiling_face: !", user)

            
            elif message == "?" or message == "help":
                mes = "Options \nHelp - Display Help And Commands \nClients or Customers - Show Active Clients\nTask - " \
                      "Submit a task\nRandom - Proof That Im Not A Boring Bot :stuck_out_tongue_winking_eye: \n\nType Usage for usage options\nThis is beta version , " \
                      "for any errors contact the cat."
                send_message(mes, user)
            
            elif message == "usage":
                send_message("task,Username,Client,Activity,Department,Message,Time\nExample: task,George,Nestle,Development,Marketing,Example,2.30\nMake sure you type each field "
                             "the right way :wink:",
                             user)
            
            elif message == "clients" or message == "customers":
                send_message(str(clients).replace('[', '').replace(']', ''), user)
            
            elif message.__contains__("task"):
                try:
                    task, user, client, activity, department, usr_message, time_worked = message.split(',')
                    
                    if client in clients and activity in activities and department in departments and time_worked.isdigit():
                        try:
                            info = (user, client, activity, department, usr_message, time_worked)
                            cur.execute("INSERT INTO tasks(username,client,activity,department,usr_message,time_worked) VALUES (?, ?, ?, ?, ?, ?)", info)
                            cn.commit()
                        except:
                            print "Unexpected error:", sys.exc_info()[0]
                    else:
                        send_message("The information you entered is not valid! :confused:", user)
                except ValueError:
                    send_message("Not Enough Information \nPlease Follow This Example : task,Username,Client,Activity,Department,Message,Time\nExample: task,George,Nestle,"
                                 "Development,Marketing,Example,2.30", user)
            
            elif message == "whoami":
                send_message("Your id is : " + user + " :sunglasses:", user)
            
            elif message == "show entries":
                # Admin ID
                if user == admin:
                    cur.execute('''SELECT * FROM tasks''')
                    for row in cur:
                        send_message(row, user)
                        time.sleep(0.3)
                else:
                    send_message("You do not have permission to view the database!", user)
            
            elif message == "random":
                send_message(random.choice(randomfacts), user)
            
            elif message == "why":
                send_message("Cause i say it! :sunglasses:", user)
            
            elif message == "ok":
                send_message("okay!", user)
            
            else:
                continue

else:
    print "Connection Failed, Check your token and make sure you activate virtual environment!"
