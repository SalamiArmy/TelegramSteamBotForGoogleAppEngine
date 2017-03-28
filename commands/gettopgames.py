# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, chat_id, user):
    gameResults = get_steam_top_games().encode('utf-8')
    if gameResults:
        bot.sendMessage(chat_id=chat_id, text=gameResults,
                        disable_web_page_preview=True, parse_mode='Markdown')
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any top selling steam games.')


def get_steam_top_games():
    rawMarkup = urllib.urlopen('http://store.steampowered.com/search/?filter=topsellers').read()
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    hot_games = '*Top Selling Steam Games:*'
    for resultRow in soup.findAll('span', attrs={'class':'title'}):
        hot_games += '\n' + resultRow.text.replace('_', ' ').replace('`', '').replace('*', '')
    return hot_games

def steam_game_name_parser(code, link):
    soup = BeautifulSoup(code, 'html.parser')

    titleDiv = soup.find('div', attrs={'class':'apphub_AppName'})
    if titleDiv:
        gameTitle = titleDiv.string
        return gameTitle
    else:
        return ''
