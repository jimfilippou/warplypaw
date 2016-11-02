# WarplyPaw Version 1.3 (Wednesday 2 November 2016)

from slackclient import *
import sqlite3, os, time, sys, datetime, random

randomfacts=[
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
    "China has more English speakers than the United States.",
    "The longest time between two twins being born is 87 days.",
    "n 2007, an American man named Corey Taylor tried to fake his own death in order to get out of his cell phone contract without paying a fee. It didn't work.",
    "Everyone has a unique tongue print, just like fingerprints.",
    "Most Muppets are left-handed. (Because most Muppeteers are right-handed, so they operate the head with their favoured hand.)",
    "Female kangaroos have three vaginas.",
    "In 1567, the man said to have the longest beard in the world died after he tripped over his beard running away from a fire.",
    "The top of the Eiffel Tower leans away from the sun, as the metal facing the sun heats up and expands. It can move as much as 7 inches.",
    "There are around 60,000 miles of blood vessels in the human body. If you took them all out and laid them end to end, they'd stretch around the world more than twice. But, seriously, don't do that either.",
    "95% of people text things they could never say in person",
    "Nobody knows warply's cat name.",
    "It is impossible to lick your elbow",
    "People say Bless you when you sneeze because when you sneeze,your heart stops for a mili-second",
    "It is physically impossible for pigs to look up into the sky",
    "Over 75% of people who read this will try to lick their elbow.",
    "Bill Gates' first business was Traff-O-Data, a company that created machines which recorded the number of cars passing a given point on a road.",
    "Donald Duck comics were banned from Finland because he doesn't wear any pants.",
    "Ketchup was sold in the 1830s as medicine.",
    "There are no clocks in Las Vegas gambling casinos.",
    "Chewing gum while peeling onions will keep you from crying!",
    "You can’t kill yourself by holding your breath",
    "Your heart beats over 100,000 times a day"
]

# Global Variables
# BOT_ID = os.environ.get("BOT_ID")
token = os.environ.get('SLACK_BOT_TOKEN')
admins = []

# Create SQLite Database
cn = sqlite3.connect(':memory:')
print('Database Is Running On Memory!')

# Create SQLite Cursor
cur = cn.cursor()

# Create Table For Tasks
try:
    cur.execute('''CREATE TABLE tasks(id INTEGER PRIMARY KEY, username TEXT, client TEXT, activity TEXT, department TEXT, usr_message TEXT, time_worked)''')
    print('Table Created!.')
except sqlite3.OperationalError:
    print('Table is already created!.')


# Bot Functions
def send_message(msg, chnl):
    sc.api_call("chat.postMessage", channel=chnl, text=msg, username="WarplyPaw", as_user="WarplyPaw")

# Customers
clients = ["eurobank", "nestle", "nag", "nbginsurance" , "heineken", "cnn", "carefour", "dominos"]
activities = ["development", "testing", "designing"]
departments = ["delivery", "marketing", "design"]

# Tracking 
log_file = open("Activity.log", "w")
log_file.write("------------* LOG FILE *-------------")
i = datetime.datetime.now()
date = "%s/%s/%s : %s:%s:%s" % (i.year, i.month, i.day , i.hour, i.minute, i.second)

# Slack Object
sc = SlackClient(token)
if sc.rtm_connect():
    print('Bot Started !')
    log_file.write("\n[%s] Bot Started!" % (date))
    while True:
        try:
            for slack_message in sc.rtm_read():
                
                message = slack_message.get("text")
                user = slack_message.get("user")
                
                if not message or not user:
                    continue
                    
                message = message.lower()
                i = datetime.datetime.now()
                date = "%s/%s/%s : %s:%s:%s" % (i.year, i.month, i.day , i.hour, i.minute, i.second)
                log_file.write("%s Recieved" % (message))
                
                if message.__contains__("hello") or message.__contains__("hi") or message.__contains__("hey"):
                    send_message("Hello There Human :feet: !", user)
                    
                elif message == "?" or message == "help":
                    mes = "Options \nHelp - Display Help And Commands \nClients or Customers - Show Active Clients\nTask - " \
                          "Submit a task\nRandom - Proof That Im Not A Boring Bot :stuck_out_tongue_winking_eye: \n\nType Usage for usage options\nThis is beta version , " \
                          "for any errors contact the cat."
                    send_message(mes, user)
                    
                elif message == "usage":
                    send_message("task/Username/Client/Activity/Department/Message/Time\nExample: task/George/Nestle/Development/Marketing/Example/2.30\nMake sure you type each field "
                                 "the right way :wink:",
                                 user)
                    
                elif message == "clients" or message == "customers":
                    send_message(str(clients).replace('[', '').replace(']', ''), user)
                    
                elif message.__contains__("task"):
                    try:
                        task, user, client, activity, department, usr_message, time_worked = message.split('/')
                        if client in clients and activity in activities and department in departments and time_worked.isdigit():
                            try:
                                info = (user, client, activity, department, usr_message, time_worked)
                                cur.execute("INSERT INTO tasks(username,client,activity,department,usr_message,time_worked) VALUES (?, ?, ?, ?, ?, ?)", info)
                                cn.commit()
                            except:
                                log_file.write("Unexpected error:" + sys.exc_info()[0])
                        else:
                            send_message("The information you entered is not valid! :confused:", user)
                            
                    except ValueError:
                        send_message("Not Enough Information \nPlease Follow This Example : task,Username,Client,Activity,Department,Message,Time\nExample: task,George,Nestle,"
                                     "Development,Marketing,Example,2.30", user)
                elif message == "whoami":
                    send_message("Your id is : " + user + " :sunglasses:", user)

                elif message == "show entries":
                    if user in admins:
                        cur.execute('''SELECT * FROM tasks''')
                        for row in cur:
                            send_message(row, user)
                            time.sleep(0.4)
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
        except Exception:
            log_file.write("[%s] Unexpected error => " % (date), sys.exc_info()[0])
            log_file.close()
else:
    log_file.write("\n[%s] Failed To Connect" % (date))
    log_file.close()
    print "Connection Failed\nPossible Errors: \n1.Invalid Token\n2.Deactivated Virtual Environment\n3.No Internet Connection"
