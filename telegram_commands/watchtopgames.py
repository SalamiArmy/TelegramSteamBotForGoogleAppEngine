# coding=utf-8
import main

from google.appengine.ext import ndb

from telegram_commands.gettopgames import get_steam_top_games

watchedCommandName = 'gettopgames'.encode('utf-8')
removed_games_title = '\n*Removed Games:*'.encode('utf-8')
added_games_title = '\n*New Games:*'.encode('utf-8')
newly_added_games_title = '\n(beta)*New New Games:*'.encode('utf-8')


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
        es.allPreviousAddedTitles += '\n' + str(NewValue)
    else:
        es.allPreviousAddedTitles += NewValue
    es.put()


def getWatchValue(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return es.currentValue.encode('utf-8')
    return ''


def getPreviouslyAddedTitlesValue(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousAddedTitles.encode('utf-8')
    return ''

def wasPreviouslyAddedTitle(chat_id, game_title):
    allPreviousGames = getPreviouslyAddedTitlesValue(chat_id)
    if '\n' + game_title + '\n' in allPreviousGames or \
        allPreviousGames.startswith(game_title + '\n') or  \
        allPreviousGames.endswith('\n' + game_title) or  \
        allPreviousGames == game_title:
        return True;
    return False;


def get_add_removed_games(chat_id, new_list, old_list):
    added_games = added_games_title
    newly_added_games = newly_added_games_title
    for item in new_list.split('\n'):
        if item not in old_list:
            added_games += '\n' + item
            if not wasPreviouslyAddedTitle(chat_id, item):
                addPreviouslyAddedTitlesValue(chat_id, item)
                newly_added_games += '\n' + item
    removed_games = removed_games_title
    for item in old_list.split('\n'):
        if item not in new_list:
            removed_games += '\n' + item
    return added_games, removed_games, newly_added_games


def run(bot, chat_id, user, keyConfig='', message=''):
    top_games = get_steam_top_games().encode('utf-8')
    if top_games:
        OldValue = getWatchValue(chat_id)
        if OldValue != top_games:
            setWatchValue(chat_id, top_games)
            if OldValue == '':
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Now watching /' + watchedCommandName+ '\n' + top_games,
                                    parse_mode='Markdown')
            else:
                games_added, games_removed, newly_added_games = get_add_removed_games(chat_id, top_games, OldValue)
                message_text = 'Watch for /' + watchedCommandName + ' has changed' + (' order.' if (
                games_added == added_games_title and games_removed == removed_games_title) else '.') + '\n' + top_games + (
                        '\n' + games_added if games_added != added_games_title else '') + (
                        '\n' + games_removed if games_removed != removed_games_title else '') + (
                        '\n' + newly_added_games if newly_added_games != newly_added_games_title else '')
                bot.sendMessage(chat_id=chat_id,
                                text=message_text,
                                parse_mode='Markdown')
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' has not changed:\n' + top_games,
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
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ',' in watches or ',' + str(chat_id) + ':' + watchedCommandName in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + watchedCommandName)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' not found.')
    if getWatchValue(chat_id) != '':
        setWatchValue(chat_id, '')
