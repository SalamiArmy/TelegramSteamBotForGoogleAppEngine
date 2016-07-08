import ConfigParser
import unittest

import telegram

import commands.getgame as getgame


class TestGetGame(unittest.TestCase):
    def test_getgame_with_suerhot(self):
        requestText = 'SUPERHOT'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_vrregatta(self):
        requestText = 'VR Regatta'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_halflife1a(self):
        requestText = 'Half-Life 1'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_csgo(self):
        requestText = 'csgo'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)
