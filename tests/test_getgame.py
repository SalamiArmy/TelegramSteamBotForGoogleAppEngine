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

    def test_getgame_with_halflife1(self):
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

    def test_getgame_with_cs(self):
        requestText = 'cs'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_rawdata(self):
        requestText = 'raw data'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_wehappyfew(self):
        requestText = 'we happy few'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_shadowwarrior(self):
        requestText = 'shadow warrior'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_blank(self):
        requestText = ''

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_thisisthepolice(self):
        requestText = 'this is the police'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_mysummercar(self):
        requestText = 'my summer car'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)

    def test_getgame_with_blank(self):
        requestText = ''

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', requestText)