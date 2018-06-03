# coding=utf-8
import ConfigParser
import unittest

import telegram

from web_commands.getpopgames import run


class TestGetGame(unittest.TestCase):
    def test_getpopgames(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        run(bot, chatId, 'Admin')
