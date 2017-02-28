import ConfigParser
import unittest

import telegram

import commands.NumberOfTimesVisitted as NumberOfTimesVisitted


class TestGetGame(unittest.TestCase):
    def test_NumberOfTimesVisitted(self):
        requestText = '429490'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        NumberOfTimesVisitted.run(bot, chatId, 'Admin', requestText)