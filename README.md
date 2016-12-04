# WarplyPaw

Author : Dimitris Filippou

!["Text"](https://media.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAAe4AAAAJDFmMGQ5ODI2LWI4ZmItNDRlOC1iZmRjLTNmZDk2N2NkMTA0Mw.png "Warply")

#Warply Smart Bot

WarplyPaw is our company's automation slack bot , he is a cat and lives under our servers. 

#Installing Bot
###Getting Our Environment Ready
Go to the terminal (or Command Prompt on Windows) and change into the directory where you want to store this project. Within that directory, create a new virtualenv to isolate our application dependencies from other Python projects.

```bash
virtualenv slacktimesheets 
```
Activate the virtualenv:
```bash
source slacktimesheets/bin/activate 
```

The official slackclient API library built by Slack can send and receive messages from Slack. Install the slackclient library with this command:

```bash
pip install slackclient
```

We also need to obtain an access token for our Slack team so our bot can use it to connect to the Slack API.
Navigate to https://api.slack.com/bot-users , and under the "Custom bot users" Section click on the "creating a new bot user" Link

Name your bot "warplytimesheets" then click the “Add bot integration” button.

The page will reload and you will see a newly-generated access token. You can also change the logo to a custom design. For example, I gave this bot the Robot Cat logo.

Click the "Save Integration" button at the bottom of the page. Your bot is now ready to connect to Slack's API.

A common practice for Python developers is to export secret tokens as environment variables. Export the Slack token with the name SLACK_BOT_TOKEN:

```bash
export SLACK_BOT_TOKEN='your slack token here'
```

Great, now we are authorized to use the Slack API as a bot.

Now everything is ready to go , launch your Bot with this command
```bash
python WarplyPaw.py
```

