# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup

from commands import addhotgame

def run(bot, chat_id, user, message):
    totalPages = int(message)
    appIds = get_results_list(totalPages)

    if appIds:
        bot.sendMessage(chat_id=chat_id, text="Top App IDs:\n" + appIds,
                        disable_web_page_preview=True, parse_mode='Markdown')
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any hot steam games.')


def get_results_list(totalPages):
    resultsListLength = 0
    pageIndex = 1
    while (pageIndex <= totalPages):
        rawMarkup = urllib.urlopen('http://store.steampowered.com/search/?filter=topsellers&category1=998&page=' + str(pageIndex)).read()
        soup = BeautifulSoup(rawMarkup, 'html.parser')
        resultList = []
        for resultRow in soup.findAll('a', attrs={'class':'search_result_row'}):
            if 'data-ds-appid' in resultRow.attrs:
                resultList.append(resultRow['data-ds-appid'])
            if 'data-ds-bundleid' in resultRow.attrs:
                resultList.append(resultRow['data-ds-bundleid'])
        resultsListLength += len(resultList)
        pageIndex += 1

    if resultsListLength > 0:
        SearchResultsInterator = 0
        ResultsCSV = ""
        while (SearchResultsInterator<resultsListLength):
            ResultsCSV += "," + resultList[SearchResultsInterator]
            SearchResultsInterator += 1
        return ResultsCSV.lstrip(",")
    return None