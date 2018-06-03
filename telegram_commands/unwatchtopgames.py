# coding=utf-8
from telegram_commands.watchtopgames import unwatch

def run(bot, chat_id, user, keyConfig='', message=''):
    unwatch(bot, chat_id)


