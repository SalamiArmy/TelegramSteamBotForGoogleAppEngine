# coding=utf-8
from google.appengine.ext import ndb


def run(bot, chat_id, user):
    hotgame = ndb.TextProperty(indexed=False, default=False)
