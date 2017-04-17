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

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardHide, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from finder import Finder
from downloader import Downloader
from sender import Sender
from converter import Converter
import os
import sys
import unicodedata
from uuid import uuid4


reload(sys)
sys.setdefaultencoding('utf-8')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

finder = Finder()
downloader = Downloader()
converter = Converter()
sender = Sender("bookfinder1301@gmail.com", "windows123")
books = dict()
emails = dict()

ERROR_MESSAGE = "Some error occurred. Please try again"


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def set_email(bot, update, args):
    if not args:
        update.message.reply_text('Please insert an email')
    else:
        email = args[0]
        chat_id = update.message.chat_id
        emails[chat_id] = email
        update.message.reply_text('Your email was updated')

def start(bot, update):
    update.message.reply_text('Hi!')

def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)

def top(bot, update):
    chat_id = update.message.chat_id
    try:
        logging.info("Searching top books")
        page = finder.top()
        books[chat_id] = page
        keyboard = [[InlineKeyboardButton(str(ind) + ". " + book.name + ", " + book.author, callback_data=str(ind))] for ind, book in enumerate(page.books)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please select your book: If you want a summary of one of the books available please insert /summary [book_number]', reply_markup=reply_markup)
        #text = "\n".join([book.name + ", " + book.author + " -> /send " + str(ind) + ", /summary " + str(ind) for ind, book in enumerate(page.books)])
    except Exception as e:
        logging.error(e, exc_info=True)
        text = ERROR_MESSAGE + " " + e.message
        bot.sendMessage(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)

def find(bot, update, args): 
    chat_id = update.message.chat_id
    if not (chat_id in emails):
        bot.sendMessage(chat_id=chat_id, text='Please set up a new email', parse_mode=ParseMode.MARKDOWN)   
    elif not args:
        bot.sendMessage(chat_id=chat_id, text='Please insert the name of the book', parse_mode=ParseMode.MARKDOWN)
    else:
        book_name = remove_accents(" ".join(args))
        logging.info("Searching books with name " + book_name)  
        try:
            page = finder.find(book_name)
            books[chat_id] = page
            #text = "\n".join([book.name + ", " + book.author + " -> /send " + str(ind) + ", /summary " + str(ind) for ind, book in enumerate(page.books)])
            keyboard = [[InlineKeyboardButton(str(ind) + ". " + book.name + ", " + book.author, callback_data=str(ind))] for ind, book in enumerate(page.books)]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Please select your book: If you want a summary of one of the books available please insert /summary [book_number]', reply_markup=reply_markup)
        except Exception as e:
            logging.error(e, exc_info=True)
            text = ERROR_MESSAGE + " " + e.message
            bot.sendMessage(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)

def more(bot, update):
    chat_id = update.message.chat_id
    logging.info("Searching more books")
    try:
        if chat_id in books:
            next_page = books[chat_id].next_page
            page = finder.more(next_page)
            books[chat_id] = page
            keyboard = [[InlineKeyboardButton(str(ind) + ". " + book.name + ", " + book.author, callback_data=str(ind))] for ind, book in enumerate(page.books)]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Please select your book: If you want a summary of one of the books available please insert /summary [book_number]', reply_markup=reply_markup)
            #text = "\n".join([book.name + ", " + book.author + " -> /send " + str(ind) + ", /summary " + str(ind) for ind, book in enumerate(page.books)])
        else:
            update.message.reply_text("First you have to search a book")
            #text = "First you have to search a book" 
    except Exception as e:
        logging.error(e, exc_info=True)
        text = ERROR_MESSAGE + " " + e.message
        bot.sendMessage(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)
   
def summary(bot, update, args):
    if not args:
        update.message.reply_text("Please insert the number of the book you want to see. For example: /summary 0") 
    chat_id = update.message.chat_id
    logging.info("Showing description for " + books[chat_id].books[int(args[0])].name)
    try:
        if chat_id in books:
            book_selected = books[chat_id].books[int(args[0])]
            description = finder.summary(book_selected)
            update.message.reply_text(description)
        else:
            update.message.reply_text("First you have to search a book") 
    except Exception as e:
        logging.error(e, exc_info=True)
        update.message.reply_text(ERROR_MESSAGE + " " + e.message) 
   
def send(bot, update):
    query = update.callback_query
    number = int(query.data)
    #if not args:
    #    update.message.reply_text("Please insert the number of the book you want to download. For example: /send 0") 
    #else:   
    chat_id = query.message.chat_id
    logging.info("Sending book " + books[chat_id].books[number].name)
    try:
        if chat_id in books:
            book_selected = books[chat_id].books[number]
            magnet_link = finder.magnet_link(book_selected)
            file_name = converter.convert(downloader.download(magnet_link))
            sender.send(emails[chat_id], file_name)
            bot.sendMessage(chat_id=chat_id, text="Your book was sent to " + emails[chat_id], parse_mode=ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id=chat_id, text="First you have to search a book" + emails[chat_id], parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logging.error(e, exc_info=True)
        bot.sendMessage(chat_id=chat_id, text=ERROR_MESSAGE + " " + e.message, parse_mode=ParseMode.MARKDOWN)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def main():
    # Create the EventHandler and pass it your bot's token.
    TOKEN = "276182891:AAFSbuNoa3HaJC2sK4ApCJdQhZfQJePnOZs"
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("top", top))
    dp.add_handler(CommandHandler("more", more))
    dp.add_handler(CommandHandler("find", find, pass_args=True))
    dp.add_handler(CommandHandler("set_email", set_email, pass_args=True))
    #dp.add_handler(CommandHandler("send", send, pass_args=True))
    dp.add_handler(CallbackQueryHandler(send))
    dp.add_handler(CommandHandler("summary", summary, pass_args=True))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # updater.start_webhook(listen="0.0.0.0",
    #                   port=8080,
    #                   url_path=TOKEN)
    # updater.bot.setWebhook("https://bookfinder1301.herokuapp.com/" + TOKEN)

    # Start the Bot
    updater.start_polling()

    #PORT = int(os.environ.get('PORT', '5000'))

    #updater.start_webhook(listen="0.0.0.0",
    #                  port=PORT,
    #                  url_path=TOKEN)
    #updater.bot.setWebhook("https://bookfinder1301.herokuapp.com/" + TOKEN)

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()