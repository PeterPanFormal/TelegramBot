#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 本bot代码修改自 python-telegram-bot/examples/echobot2.py (https://github.com/python-telegram-bot/python-telegram-bot)
# This bot code has been modified from python-telegram-bot / examples / echobot2.py (https://github.com/python-telegram-bot/python-telegram-bot)

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# 开关
# switch
deleteGroupInOutMsg = 1
deleteGroupCommondMsg = 1


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def dealAll(bot, update):
    # 删除离开群组的消息
    # Delete messages leaving the group
    if deleteGroupInOutMsg == 1 and update.message.chat.type == "supergroup" and not update.message.left_chat_member is None:
        bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    # 删除进入群组的消息
    # Delete the message entering the group
    elif deleteGroupInOutMsg == 1 and update.message.chat.type == "supergroup" and len(update.message.new_chat_members) > 0:
        bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    # 删除/号开头的命令消息
    # Delete the / at the beginning of the command message
    elif deleteGroupCommondMsg == 1 and update.message.chat.type == "supergroup" and update.message.text.startswith('/'):
        bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    # 这里将你的bot的token填写进来 替换"YOUR TOKEN"
    updater = Updater(token="YOUR TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.all,dealAll))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
