# coding=utf-8

import ConfigParser

import telegram

import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import commands.watchpopgames as watchpopgames

class TestWatchBitcoin(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_watchtopgames_with_addremovedgames(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        watchpopgames.addPreviouslyAddedTitlesValue(chatId, 'PAYDAY 2\nClicker Heroes\nStellaris\nTerraria\nFactorio\n7 Days to Die\nBlack Desert Online\nLeft 4 Dead 2\nStardew Valley\nPath of Exile\nXCOM 2\nThe Witcher 3: Wild Hunt\nTotal War: WARHAMMER\nEuro Truck Simulator 2\nDead by Daylight\nThe Elder Scrolls Online: Tamriel Unlimited\nThe Elder Scrolls V: Skyrim Special Edition\nWar Thunder\nWallpaper Engine\nEuropa Universalis IV\nHearts of Iron IV\nCities: Skylines\nFootball Manager 2016\nAge of Empires II: HD Edition\nDon\'t Starve Together\nTotal War: ROME II - Emperor Edition\nShadowverse\nWorld of Tanks Blitz\nRimWorld')
        watchpopgames.run(bot, chatId, 'SalamiArmy')
