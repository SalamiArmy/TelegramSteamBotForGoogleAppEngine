# coding=utf-8
import ConfigParser
import unittest

import telegram

import web_commands.getgame as getgame


class TestGetGame(unittest.TestCase):
    def test_getgame_with_superhot(self):
        requestText = 'The Elder Scrolls Online: Tamriel Unlimited'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, -55348600, 'Admin', keyConfig, requestText)

    def test_getgame_with_vrregatta(self):
        requestText = 'VR Regatta'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_halflife1(self):
        requestText = 'Half-Life 1'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_csgo(self):
        requestText = 'csgo'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_cs(self):
        requestText = 'cs'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_rawdata(self):
        requestText = 'raw data'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_wehappyfew(self):
        requestText = 'we happy few'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_shadowwarrior(self):
        requestText = 'shadow warrior'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_blank(self):
        requestText = ''

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_thisisthepolice(self):
        requestText = 'this is the police'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_mysummercar(self):
        requestText = 'my summer car'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_blank(self):
        requestText = ''

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_unreal_tournament(self):
        requestText = 'Unreal Tournament 2004'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_gholf_it(self):
        requestText = 'gholf it!'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_LEGO_MARVEL_Super_Heroes(self):
        requestText = u'LEGO® MARVEL Super Heroes'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_Raiders_of_the_Broken_Planet(self):
        requestText = u'Raiders of the Broken Planet'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getgame_with_back_to_bed(self):
        requestText = u'back to bed'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_PRIVATE_CHAT_ID')

        getgame.run(bot, chatId, 'Admin', keyConfig, requestText)
