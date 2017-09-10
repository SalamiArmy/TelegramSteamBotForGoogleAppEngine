# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from google.appengine.ext import ndb
from commands.getpopgames import get_steamcharts_top_games

watchedCommandName = 'getpopgames'
removed_games_title = '\n*Removed Games:*'
added_games_title = '\n*New Games:*'
newly_added_games_title = '\n(beta)*New New Games:*'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')
    allPreviousAddedTitles = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id))
    es.currentValue = NewValue
    es.put()

def addPreviouslyAddedTitlesValue(chat_id, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id))
    if (es.allPreviousAddedTitles != ''):
        print('adding ' + str(NewValue))
        es.allPreviousAddedTitles += '\n' + NewValue
    else:
        es.allPreviousAddedTitles += NewValue
    es.put()


def getWatchValue(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return str(es.currentValue)
    return ''


def getPreviouslyAddedTitlesValue(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousAddedTitles
    return ''

def wasPreviouslyAddedTitle(chat_id, game_title):
    allPreviousGames = getPreviouslyAddedTitlesValue(chat_id)
    if '\n' + game_title + '\n' in allPreviousGames or \
        allPreviousGames.startswith(game_title + '\n') or  \
        allPreviousGames.endswith('\n' + game_title) or  \
        allPreviousGames == game_title:
        return True;
    return False;


def get_added_games(chat_id, new_list, old_list):
    added_games = added_games_title
    for item in new_list.split('\n'):
        if item not in old_list and not wasPreviouslyAddedTitle(chat_id, item):
            added_games += '\n' + item
            if not wasPreviouslyAddedTitle(chat_id, item):
                addPreviouslyAddedTitlesValue(chat_id, item)
    return added_games


def run(bot, chat_id, user, keyConfig='', message=''):
    pop_games = get_steamcharts_top_games(20).encode('utf-8')
    if pop_games:
        setWatchValue(chat_id, pop_games)
        OldValue = getWatchValue(chat_id)
        games_added = get_added_games(chat_id, pop_games, OldValue)
        if games_added != added_games_title:
            if OldValue == '':
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Now watching /' + watchedCommandName,
                                    parse_mode='Markdown')
            else:
                if games_added != added_games_title:
                    message_text = 'Watch for /' + watchedCommandName + ' has changed\n' + games_added
                    bot.sendMessage(chat_id=chat_id,
                                    text=message_text,
                                    parse_mode='Markdown')
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' has not changed.',
                                parse_mode='Markdown')
        import main
        if not main.AllWatchesContains(watchedCommandName, chat_id):
            main.addToAllWatches(watchedCommandName, chat_id)
    else:
        bot.sendMessage(chat_id=chat_id,
                        text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                             ', I\'m afraid I can\'t watch ' +
                             'because I did not find any results from /' + watchedCommandName,
                        parse_mode='Markdown')


def unwatch(bot, chat_id):
    import main
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ',' in watches or ',' + str(chat_id) + ':' + watchedCommandName in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + watchedCommandName)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' not found.')
    if getWatchValue(chat_id) != '':
        setWatchValue(chat_id, '')
