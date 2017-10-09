# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib
from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig='', message='', totalResults=1):
    gameResults = get_steamcharts_top_games()
    if gameResults:
        bot.sendMessage(chat_id=chat_id, text=gameResults,
                        disable_web_page_preview=True, parse_mode='Markdown')
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any popular steam games.')


def get_steamcharts_top_games(total_pages=1):
    game_names = '*Most Popular Steam Games:*'
    for i in range(0, total_pages):
        rawMarkup = urllib.urlopen('http://steamcharts.com/top/p.' + str(i+1)).read()
        game_names += parse_game_names(rawMarkup)
    return game_names

def parse_game_names(rawMarkup):
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    game_names = ''
    for resultRow in soup.findAll('td', attrs={'class': 'game-name left'}):
        game_names += '\n' + resultRow.text.replace('\n', '').replace('\t', '').replace('_', ' ').replace('`', '').replace('*', '')
    return game_names


def steam_game_name_parser(code, link):
    soup = BeautifulSoup(code, 'html.parser')

    titleDiv = soup.find('div', attrs={'class':'apphub_AppName'})
    if titleDiv:
        gameTitle = titleDiv.string
        return gameTitle
    else:
        return ''
