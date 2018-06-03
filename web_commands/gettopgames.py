# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib

from bs4 import BeautifulSoup


def run(keyConfig='', message='', totalResults=1):
    gameResults = get_steam_top_games().encode('utf-8')
    if gameResults:
        return gameResults
    else:
        return 'I\'m sorry Dave, I\'m afraid I can\'t find any top selling steam games.'


def get_steam_top_games():
    rawMarkup = urllib.urlopen('http://store.steampowered.com/search/?filter=topsellers').read()
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    top_games = '*Top Selling Steam Games:*'
    for resultRow in soup.findAll('span', attrs={'class':'title'}):
        top_games += '\n' + resultRow.text.replace('\n', '').replace('\t', '').replace('_', ' ').replace('`', '').replace('*', '')
    return top_games
