# coding=utf-8
import string

import sys
from google.appengine.ext import ndb

class SetValue(ndb.Model):
    # key name: str(chat_id)
    theValue = ndb.StringProperty(indexed=False, default='')


# ================================

def resetSetValue(chat_id):
    es = SetValue.get_or_insert(str(chat_id))
    es.theValue = ''
    es.put()

def getSetValue(chat_id):
    es = SetValue.get_by_id(str(chat_id))
    if es:
        return es.theValue
    return ''

def run(bot, chat_id, user):
    try:
        OldValue = getSetValue(chat_id)
        if OldValue == '':
            OldValue = 'blank'
        resetSetValue(chat_id)
        bot.sendMessage(chat_id=chat_id, text='Chat ' + str(chat_id) + ' was:\n' + OldValue + '\nHas been reset.')
    except:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t reset.\n' +
                                              sys.exc_info()[0])


