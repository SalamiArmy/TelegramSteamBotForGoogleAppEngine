# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, chat_id, user, requestText):
    if requestText != '':
        ListOfAllUpdates = bot.getUpdates()
        if requestText in ListOfAllUpdates:
            bot.sendMessage(chat_id=chat_id, text=ListOfAllUpdates[requestText])
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', You must specify the AppId of a game on Steam.')