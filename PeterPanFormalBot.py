#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 本bot代码修改自 python-telegram-bot/examples/echobot2.py (https://github.com/python-telegram-bot/python-telegram-bot)
# This bot code has been modified from python-telegram-bot / examples / echobot2.py (https://github.com/python-telegram-bot/python-telegram-bot)
# test env : CentOS7 python2.7.5

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging,string,os,sys
# python3
# from configparser import ConfigParser
# python2
import ConfigParser

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# 开关
# switch
deleteGroupInOutMsg = 1
deleteGroupCommondMsg = 1
returnPrivateChatInfo = 1
adminCommand = 1
adminId = 1
telegramToken = "1"


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def readConfig(config_file_path):
    # python2
    cf = ConfigParser.ConfigParser()
    # python3
    #cf = ConfigParser()
    cf.read(config_file_path)

    #s = cf.sections()
    #o = cf.options("baseconf")
    #v = cf.items("baseconf")

    global deleteGroupInOutMsg,deleteGroupCommondMsg,returnPrivateChatInfo,adminCommand,adminId,telegramToken
    deleteGroupInOutMsg = cf.getint("baseconf", "deleteGroupInOutMsg")
    deleteGroupCommondMsg = cf.getint("baseconf", "deleteGroupCommondMsg")
    returnPrivateChatInfo = cf.getint("baseconf", "returnPrivateChatInfo")
    adminCommand = cf.getint("baseconf", "adminCommand")
    adminId = cf.getint("baseconf", "adminId")
    telegramToken = cf.get("baseconf", "telegramToken")
    
    logger.info("load ini success : deleteGroupInOutMsg, deleteGroupCommondMsg, returnPrivateChatInfo, adminCommand, adminId, telegramToken")
    logger.info(deleteGroupInOutMsg)
    logger.info(deleteGroupCommondMsg)
    logger.info(returnPrivateChatInfo)
    logger.info(adminCommand)
    logger.info(adminId)
    logger.info(telegramToken)


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
    elif returnPrivateChatInfo == 1 and update.message.chat.type == "private" and not update.message.text.startswith('/'):
        returnMsg = "from_user:" + str(update.message.from_user)
        if not update.message.forward_from is None:
            returnMsg += "\nforward_from_user:"
            returnMsg += str(update.message.forward_from)
        update.message.reply_text(returnMsg)
    elif adminCommand == 1 and update.message.chat.type == "private" and update.message.from_user.id == adminId and  update.message.text.startswith('/'):
        if update.message.text == '/help':
            update.message.reply_text("参见:https://github.com/PeterPanFormal/TelegramBot")
        else:
            update.message.reply_text("nothing to do")


def main():
    readConfig(sys.argv[1])
    """Start the bot."""
    updater = Updater(token=telegramToken)

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
