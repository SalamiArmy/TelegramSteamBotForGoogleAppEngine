#Telegram Steam Bot for Google App Engine

Go to https://console.developers.google.com and create a Google App Engine project. Then take that project id (it will be two random words and a number eg. gorilla-something-374635) and your Telegram Bot ID which the Bot Father gave you and do the following:

1. Copy app.yaml.template and rename the copy to to app.yaml.
2. Update {GOOGLE APP ENGINE PROJECT ID} in app.yaml.
3. Copy keys.ini.template and rename the copy to keys.ini.
4. Update {Your Telegram Bot ID here} in keys.ini 
OPTIONAL:
5. Update the rest of keys.ini with keys for each command you want to use.

```bash
git clone (url for your thorin fork) ~/bot
cd ~/bot
(PATH TO PYTHON27 INSTALL)\scripts\pip.exe install -t lib python-telegram-bot bs4 xmltodict six soundcloud feedparser requests tungsten
(PATH TO GOOGLE APP ENGINE LAUNCHER INSTALL)appcfg.py -A {GOOGLE APP ENGINE PROJECT ID} update .
```

You might want to clone https://github.com/Imgur/imgurpython.git and copy out the "imgurpython" folder into that lib folder that pip created
also clone https://github.com/MycroftAI/adapt.git and copy it's "adapt" folder into the root
also run "(PATH TO PYTHON27 INSTALL)\scripts\pip.exe install -t adapt pyee" from the root
oh ja, /launch command needs a module called "dateutil", pip can't find it, GAE can't find it, I can't find it on GitHub, a better man than I can fix that, I'm out.
