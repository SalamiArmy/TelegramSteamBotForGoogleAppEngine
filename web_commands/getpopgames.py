# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib
from bs4 import BeautifulSoup


def run(keyConfig='', message='', totalResults=1):
    gameResults = get_steamcharts_top_games()
    if gameResults:
        return gameResults
    else:
        return 'I\'m sorry Dave, I\'m afraid I can\'t find any popular steam games.'


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
