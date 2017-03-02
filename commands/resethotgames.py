# coding=utf-8
import string

import sys
from google.appengine.ext import ndb

from commands.addhotgame import SetHotGame


def run(bot, chat_id, user):
    try:
        OldValue = SetHotGame.getHotGames(chat_id)
        if OldValue == '':
            OldValue = 'blank'
        SetHotGame.resetHotGames(chat_id)
        bot.sendMessage(chat_id=chat_id, text='Chat ' + str(chat_id) + ' was:\n' + OldValue + '\nHas been reset.')
    except:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t reset.\n' +
                                              sys.exc_info()[0])


