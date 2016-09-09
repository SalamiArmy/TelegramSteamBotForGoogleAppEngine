import ConfigParser
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

BASE_URL = 'https://api.telegram.org/bot'

# Read keys.ini file at program start (don't forget to put your keys in there!)
keyConfig = ConfigParser.ConfigParser()
keyConfig.read(["keys.ini", "..\keys.ini"])

bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


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
            elif text == '/gethotgame':
                try:
                    gethotgame.run(bot, str(chat_id), user)
                except:
                    print("Unexpected error running get hot game command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))


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


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/run_tests', RunTestsHandler),
    ('/run', WebCommandRunHandler)
], debug=True)
