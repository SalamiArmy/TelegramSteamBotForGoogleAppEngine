#Telegram Steam Bot for Google App Engine
This is a message bot for Telegram which is supposed to be hosted on Google App Engine for free.

##Setup Google Apps Project
Go to https://console.developers.google.com and create a Google App Engine project. Then take that project id (it might be two random words and a number eg. gorilla-something-374635 but I think they changed that) and your Telegram Bot ID which the Bot Father gave you and do the following:

1. Copy app.yaml.template and rename the copy to to app.yaml.
2. Update {GOOGLE APP ENGINE PROJECT ID} in app.yaml.
3. Copy keys.ini.template and rename the copy to keys.ini.
4. Update {Your Telegram Bot ID here} in keys.ini

##Build Telegram Bot (Do this on the CI server)
```bash
git clone (url for your TelegramSteamBotForGoogleAppEngine fork) ~/bot
cd ~/bot
(PATH TO PYTHON27 INSTALL)\scripts\pip.exe install -t lib python-telegram-bot bs4
(PATH TO GOOGLE APP ENGINE LAUNCHER INSTALL)appcfg.py -A {GOOGLE APP ENGINE PROJECT ID} update .
```

Finally, go to https://project-id.appspot.com/set_webhook?url=https://project-id.appspot.com/webhook (replace both project-ids with the {GOOGLE APP ENGINE PROJECT ID}).