import ConfigParser
import unittest

import telegram

import commands.getimgur as getimgur


class TestGetGame(unittest.TestCase):
    def test_getimgur_with(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getimgur.run(bot, keyConfig, chatId, 'Admin')