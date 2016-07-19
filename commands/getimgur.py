# coding=utf-8
import string

import telegram
from imgurpython import ImgurClient


def run(bot, keyConfig, chat_id, user):
    client_id = keyConfig.get('Imgur', 'CLIENT_ID')
    client_secret = keyConfig.get('Imgur', 'CLIENT_SECRET')
    client = ImgurClient(client_id, client_secret)
    items = client.subreddit_gallery(subreddit='pcmasterrace',
                                     sort='top',
                                     window='day')
    if len(items) > 0:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=chat_id,
                      photo=items[0].link.encode('utf-8'))
        return True
