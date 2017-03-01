# coding=utf-8
import string

import sys
from google.appengine.ext import ndb

class SetHotGame(ndb.Model):
    # key name: str(chat_id)
    previousHotGames = ndb.StringProperty(indexed=False, default='')

# ================================

def addHotGame(chat_id, NewHotGame):
    es = SetHotGame.get_or_insert(str(chat_id))
    if es.previousHotGames == '':
        es.previousHotGames = NewHotGame
    else:
        es.previousHotGames = es.previousHotGames + ',' + NewHotGame
    es.put()

def getHotGames(chat_id):
    es = SetHotGame.get_by_id(str(chat_id))
    if es:
        return es.previousHotGames
    return ''

def run(bot, chat_id, user, message):
    try:
        requestText = message.replace(bot.name, "").strip()
        OldHotGames = getHotGames(chat_id)
        if OldHotGames == '':
            OldHotGames = 'blank'
        addHotGame(chat_id, requestText)
        bot.sendMessage(chat_id=chat_id, text='Chat ' + str(chat_id) + ' contains:\n' + OldHotGames + '\nadding:\n' + requestText)
    except:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t set ' +
                                              string.capwords(requestText.encode('utf-8')) + '. ' + sys.exc_info()[0])


