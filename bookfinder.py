#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardHide, ParseMode
import logging
from finder import Finder
from downloader import Downloader
from sender import Sender
from converter import Converter

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

finder = Finder()
downloader = Downloader()
converter = Converter()
sender = Sender("bookfinder1301@gmail.com", "windows123")
books = dict()


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)

def find(bot, update, args):
    # print "Searching books with name " + " ".join(args)
    chat_id = update.message.chat_id
    available_books = finder.find(" ".join(args))
    books[chat_id] = available_books
    text = "\n".join([book.name + " -> /send " + str(ind) for ind, book in enumerate(available_books)])
    print "Books found: " + str(available_books)
    # book_names = ["Las mil y una noches", "Cien aos de soledad", "/La fundacion"]
    # update.message.reply_text("/test")
    # bot.sendMessage(chat_id=chat_id, text="*bold* /test _italic_ `fixed width font` [link](http://google.com).", parse_mode=ParseMode.MARKDOWN)
    bot.sendMessage(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)


def send(bot, update, args):
    chat_id = update.message.chat_id
    if chat_id in books:
        book_selected = books[chat_id][int(args[0])]
        magnet_link = finder.magnet_link(book_selected)
        file_name = converter.convert(downloader.download(magnet_link))
        print file_name
        sender.send(args[1], file_name)
        update.message.reply_text("Your book was sended to " + args[1])
    else:
        update.message.reply_text("First you have to search a book") 

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    TOKEN = "276182891:AAFSbuNoa3HaJC2sK4ApCJdQhZfQJePnOZs"
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("find", find, pass_args=True))
    dp.add_handler(CommandHandler("send", send, pass_args=True))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                      port=8080,
                      url_path=TOKEN)
    updater.bot.setWebhook("https://bookfinder1301.herokuapp.com/" + TOKEN)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()