import ConfigParser
import importlib
import json
import logging
import unittest
import urllib
import sys

import urllib2
import telegram
import commands.getgame as getgame
import commands.gethotgame as gethotgame

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import webapp2

from commands import gettopgames
from commands import getpopgames
from commands import watchtopgames
from commands import watchpopgames
from commands import unwatchtopgames
from commands import unwatchpopgames

BASE_URL = 'https://api.telegram.org/bot'

# Read keys.ini file at program start (don't forget to put your keys in there!)
keyConfig = ConfigParser.ConfigParser()
keyConfig.read(["keys.ini", "..\keys.ini"])

bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

# ================================

class AllWatchesValue(ndb.Model):
    # key name: AllWatches
    currentValue = ndb.StringProperty(indexed=False, default='')

# ================================

def addToAllWatches(command, chat_id, request=''):
    es = AllWatchesValue.get_or_insert('AllWatches')
    es.currentValue += ',' + str(chat_id) + ':' + command + (':' + request if request != '' else '')
    es.put()

def AllWatchesContains(command, chat_id, request=''):
    es = AllWatchesValue.get_by_id('AllWatches')
    if es:
        return (',' + str(chat_id) + ':' + command + (':' + request if request != '' else '')) in str(es.currentValue) or \
               (str(chat_id) + ':' + command + (':' + request if request != '' else '') + ',') in str(es.currentValue)
    return False

def setAllWatchesValue(NewValue):
    es = AllWatchesValue.get_or_insert('AllWatches')
    es.currentValue = NewValue
    es.put()

def getAllWatches():
    es = AllWatchesValue.get_by_id('AllWatches')
    if es:
        return es.currentValue
    return ''

def removeFromAllWatches(watch):
    setAllWatchesValue(getAllWatches().replace(',' + watch + ',', ',')
                       .replace(',' + watch, '')
                       .replace(watch + ',', ''))


# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(
            BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(
            BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(
                BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        if 'message' in body:
            message = body['message']
            text = message.get('text')
            fr = message.get('from')
            user = fr['username'] \
                if 'username' in fr \
                else fr['first_name'] + ' ' + fr['last_name'] \
                if 'first_name' in fr and 'last_name' in fr \
                else fr['first_name'] if 'first_name' in fr \
                else 'Dave'
            chat = message['chat']
            chat_id = chat['id']

            if not text:
                logging.info('no text')
                return

            text = text.replace(bot.name, '').strip()
            if text.startswith('/game'):
                split = text[1:].lower().split(" ", 1)
                try:
                    getgame.run(bot, chat_id, user, split[1] if len(split) > 1 else '')
                except:
                    print("Unexpected error running command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            elif text.startswith('/gethotgame'):
                try:
                    gethotgame.run(bot, str(chat_id), user)
                except:
                    print("Unexpected error running get hot game command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            elif text.startswith('/gettopgames'):
                split = text[1:].lower().split(" ", 1)
                try:
                    gettopgames.run(bot, str(chat_id), user, split[1] if len(split) > 1 else '')
                except:
                    print("Unexpected error running get top games command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            elif text.startswith('/getpopgames'):
                split = text[1:].lower().split(" ", 1)
                try:
                    getpopgames.run(bot, str(chat_id), user, split[1] if len(split) > 1 else '')
                except:
                    print("Unexpected error running get pop games command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            elif text.startswith('/watchtopgames'):
                split = text[1:].lower().split(" ", 1)
                try:
                    watchtopgames.run(bot, str(chat_id), user, split[1] if len(split) > 1 else '')
                except:
                    print("Unexpected error running watch top games command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            elif text.startswith('/watchpopgames'):
                split = text[1:].lower().split(" ", 1)
                try:
                    watchpopgames.run(bot, str(chat_id), user, split[1] if len(split) > 1 else '')
                except:
                    print("Unexpected error running watch pop games command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            elif text.startswith('/unwatchtopgames'):
                split = text[1:].lower().split(" ", 1)
                try:
                    unwatchtopgames.run(bot, str(chat_id), user, split[1] if len(split) > 1 else '')
                except:
                    print("Unexpected error running unwatch top games command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            elif text.startswith('/unwatchpopgames'):
                split = text[1:].lower().split(" ", 1)
                try:
                    unwatchpopgames.run(bot, str(chat_id), user, split[1] if len(split) > 1 else '')
                except:
                    print("Unexpected error running unwatch pop games command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))


class RunTestsHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        suite = unittest.TestSuite()

        formattedResultText = ''
        getTest = unittest.defaultTestLoader.loadTestsFromName('tests.test_getgame')
        suite.addTest(getTest)

        formattedResultText += str(unittest.TextTestRunner().run(suite))\
            .replace('<unittest.runner.TextTestResult ', '')\
            .replace('>', '')
        self.response.write(formattedResultText)


class WebCommandRunHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        text = self.request.get('text') or self.request.get('game')
        user = self.request.get('user') or 'Admin'
        if not text:
            self.response.write('Argument missing: \'text\' or \'game\'.')
            return
        chat_id = self.request.get('chat_id')
        if not chat_id:
            chat_id = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        split = text[1:].lower().split(" ", 1)
        try:
            getgame.run(bot, chat_id, user, split[1] if len(split) > 1 else '')
        except:
            print("Unexpected error running command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))


class TriggerAllWatches(webapp2.RequestHandler):
    def get(self):
        AllWatches = getAllWatches()
        watches_split = AllWatches.split(',')
        if len(watches_split) >= 1:
            for watch in watches_split:
                print('got watch ' + watch)
                split = watch.split(':')
                if len(split) >= 2:
                    print('executing command: ' + split[1].replace('get', ''))
                    mod = importlib.import_module('commands.watch' + split[1].replace('get', ''))
                    chat_id = split[0]
                    request_text = (split[2] if len(split) == 3 else '')
                    mod.run(bot, keyConfig, chat_id, 'Watcher', request_text)
                else:
                    print('removing from all watches: ' + watch)
                    removeFromAllWatches(watch)

class ClearAllWatches(webapp2.RequestHandler):
    def get(self):
        setAllWatchesValue('')


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/run_tests', RunTestsHandler),
    ('/run', WebCommandRunHandler),
    ('/allwatches', TriggerAllWatches),
    ('/clearallwatches', ClearAllWatches)
], debug=True)
