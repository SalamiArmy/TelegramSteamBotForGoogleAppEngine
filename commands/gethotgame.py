# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup

from commands import addhotgame
from commands import getgame

def HasBeenAHotGame(chat_id, game):
    hotGame = addhotgame.getHotGames(chat_id)
    return hotGame.startswith(game + ",") or ("," + game + "," in hotGame) or (hotGame.endswith("," + game))

def run(bot, chat_id, user):
    appId = steam_results_parser(chat_id)

    if appId:
        steamGameLink = 'http://store.steampowered.com/app/' + appId
        bypassAgeGate = urllib2.build_opener()
        bypassAgeGate.addheaders.append(('Cookie', 'birthtime=578390401'))
        code = bypassAgeGate.open(steamGameLink).read()
        if 'id=\"app_agegate\"' in code:
            gameTitle = getgame.steam_age_gate_parser(code)
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid that \"' + gameTitle + '\" is protected by an age gate and cannot be featured.')
            return False

        gameResults = getgame.steam_game_parser(code, steamGameLink)
        bot.sendMessage(chat_id=chat_id, text=gameResults,
                        disable_web_page_preview=True, parse_mode='Markdown')
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any hot steam games to feature.')


def steam_results_parser(chat_id):
    pageIndex = 1
    while (pageIndex <= 250):
        rawMarkup = urllib.urlopen('http://store.steampowered.com/search/?filter=topsellers&category1=998&page=' + str(pageIndex)).read()
        soup = BeautifulSoup(rawMarkup, 'html.parser')
        for resultRow in soup.findAll('a', attrs={'class':'search_result_row'}):
            if 'data-ds-appid' in resultRow.attrs:
                foundAppId = resultRow['data-ds-appid']
                if not (HasBeenAHotGame(chat_id, foundAppId)):
                    addhotgame.addHotGame(chat_id, foundAppId)
                    return foundAppId
            if 'data-ds-bundleid' in resultRow.attrs:
                foundAppId = resultRow['data-ds-bundleid']
                if not (HasBeenAHotGame(chat_id, foundAppId)):
                    addhotgame.addHotGame(chat_id, foundAppId)
                    return foundAppId
        pageIndex += 1