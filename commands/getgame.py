# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, chat_id, user, requestText):
    if requestText == '':
        rawMarkup = urllib.urlopen('http://store.steampowered.com/search/?category1=998&term=#').read()
        totalGames = steam_all_results_parser(rawMarkup)
        if totalGames != '':
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                  ', there are ' + totalGames + ' total games on steam. Pick one.')
            return True

    retryCount = 3
    appId = ''
    while retryCount > 0 and appId == '':
        retryCount -= 1
        rawMarkup = urllib.urlopen('http://store.steampowered.com/search/?category1=998&term=' + requestText).read()
        appId = steam_results_parser(rawMarkup)

    if appId:
        steamGameLink = 'http://store.steampowered.com/app/' + appId
        bypassAgeGate = urllib2.build_opener()
        bypassAgeGate.addheaders.append(('Cookie', 'birthtime=578390401'))
        code = bypassAgeGate.open(steamGameLink).read()
        if 'id=\"app_agegate\"' in code:
            gameTitle = steam_age_gate_parser(code)
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid that \"' + gameTitle + '\" is protected by an age gate.')
            return False

        gameResults = steam_game_parser(code, steamGameLink)
        bot.sendMessage(chat_id=chat_id, text=gameResults,
                        disable_web_page_preview=True, parse_mode='Markdown')
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find the steam game ' + \
                                              requestText.encode('utf-8'))


def steam_results_parser(rawMarkup):
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    resultList = []
    for resultRow in soup.findAll('a', attrs={'class':'search_result_row'}):
        if 'data-ds-appid' in resultRow.attrs:
            resultList.append(resultRow['data-ds-appid'])
        if 'data-ds-bundleid' in resultRow.attrs:
            resultList.append(resultRow['data-ds-bundleid'])
    if len(resultList) > 0:
        return resultList[0]
    return ''

def steam_all_results_parser(rawMarkup):
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    rawPaginationString = soup.find('div', attrs={'class':'search_pagination_left'}).string
    return rawPaginationString.replace('showing 1 - 25 of', '').strip()

def steam_age_gate_parser(rawMarkup):
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    rawTitleString = soup.find('title').string
    return rawTitleString.strip()

def steam_game_parser(code, link):
    soup = BeautifulSoup(code, 'html.parser')
    AllGameDetailsFormatted = ''

    titleDiv = soup.find('div', attrs={'class':'apphub_AppName'})
    if titleDiv:
        gameTitle = titleDiv.string
        AllGameDetailsFormatted += '*' + gameTitle

    priceDiv = soup.find('div', attrs={'class':'game_purchase_price price'})
    if priceDiv:
        gamePrice = priceDiv.string
        AllGameDetailsFormatted += ' - ' + gamePrice.strip()
    else:
        priceDiv = soup.find('div', attrs={'class':'discount_final_price'})
        if priceDiv:
            gamePrice = priceDiv.string
            AllGameDetailsFormatted += ' - ' + gamePrice.strip()
            discountPercentageDiv = soup.find('div', attrs={'class':'discount_pct'})
            if discountPercentageDiv:
                percentageDiscountedBy = discountPercentageDiv.string
                AllGameDetailsFormatted += ' (at ' + percentageDiscountedBy.strip() + ' off)'
    AllGameDetailsFormatted += '*\n'

    descriptionDiv = soup.find('div', attrs={'class':'game_description_snippet'})
    if descriptionDiv:
        descriptionSnippet = descriptionDiv.string.replace('\r', '').replace('\n', '').replace('\t', '').replace('_', ' ')
        AllGameDetailsFormatted += descriptionSnippet + '\n'

    if AllGameDetailsFormatted:
        AllGameDetailsFormatted += link + '\n'

    dateSpan = soup.find('span', attrs={'class':'date'})
    if dateSpan:
        releaseDate = dateSpan.string
        AllGameDetailsFormatted += 'Release Date: ' + releaseDate + '\n'

    featureList = ''
    featureLinks = soup.findAll('a', attrs={'class':'name'})
    if len(featureLinks) > 0:
        for featureLink in featureLinks:
            featureList += '     ' + featureLink.string.replace('Seated', 'Seated VR') + '\n'
        AllGameDetailsFormatted += 'Features:\n' + featureList

    reviewRows = ''
    reviewDivs = soup.findAll('div', attrs={'class':'user_reviews_summary_row'})
    if len(reviewDivs) > 0:
        for reviewRow in reviewDivs:
            reviewSubtitleDiv = reviewRow.find('div', attrs={'class':'subtitle column'}).string
            reviewSummaryDiv = reviewRow.find('div', attrs={'class':'summary column'}).string
            if not reviewSummaryDiv:
                reviewSummaryDiv = reviewRow.find('span', attrs={'class':'nonresponsive_hidden responsive_reviewdesc'}).string
            reviewSummaryDiv = reviewSummaryDiv.replace('\r', '').replace('\n', '').replace('\t', '')
            if reviewSummaryDiv != 'No user reviews':
                reviewRows += '     ' + reviewSubtitleDiv + reviewSummaryDiv.replace('-', '').replace(' user reviews', '').replace(' of the ', ' of ') + '\n'
        if reviewRows:
            AllGameDetailsFormatted += 'Reviews:\n' + reviewRows
        if AllGameDetailsFormatted.endswith('\n'):
            AllGameDetailsFormatted = AllGameDetailsFormatted[:AllGameDetailsFormatted.rfind('\n')]

    tagList = ''
    tagLinks = soup.findAll('a', attrs={'class':'app_tag'})
    if len(tagLinks) > 0:
        for tagLink in tagLinks:
            tagList += tagLink.string.replace('\r', '').replace('\n', '').replace('\t', '') + ', '
        AllGameDetailsFormatted += '\n' + 'Tags:\n`' + tagList
    if AllGameDetailsFormatted.endswith(', '):
        AllGameDetailsFormatted = AllGameDetailsFormatted[:AllGameDetailsFormatted.rfind(', ')]
        AllGameDetailsFormatted += '`'

    return AllGameDetailsFormatted