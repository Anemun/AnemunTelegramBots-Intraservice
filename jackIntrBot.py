import telebot
import argparse, sys
import intraserviceProvider
from telebot import types

version = "0.1.4"

parser=argparse.ArgumentParser()
parser.add_argument('--botToken', help='telegram bot token')
parser.add_argument('--site', help='intraservice address')
parser.add_argument('--siteLogin', help='intraservice login')
parser.add_argument('--sitePass', help='intraservice password')
args=parser.parse_args()
botToken = args.botToken

bot = telebot.TeleBot(botToken)
login = args.siteLogin
password = args.sitePass
intraserviceProvider.login = login
intraserviceProvider.password = password

@bot.message_handler(commands=["start"])
def start(message):
    id = intraserviceProvider.getIntrIdByUsername(message.from_user.username)
    if id is not None:
        bot.send_message(message.chat.id, "Вы можете пользоваться ботом. Попробуйте следующие команды:\n/watcher")

@bot.message_handler(commands=["watcher"])
def getFromWatcher(message):
    if intraserviceProvider.auth(message.from_user.username) is False:
        return
    tickets = intraserviceProvider.getWatcher()
    keyboard = types.InlineKeyboardMarkup()
    for ticket in tickets:
        button = types.InlineKeyboardButton(text=ticket.title, callback_data="ticket_"+ str(ticket.id))
        keyboard.add(button)
    bot.send_message(chat_id=message.chat.id, text="Диспетчер: " + str(len(tickets)) + " заявок",reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.split('_')[0] == "ticket":
        ticketId = call.data.split('_')[1]
    ticket = intraserviceProvider.getTicketById(ticketId)
    bot.send_message(chat_id=call.message.chat.id, text="ID: {0}\nCreator: {1}\nText: {2}".format(ticket.id, ticket.creatorName, ticket.title))

if __name__ == '__main__':
    bot.polling(none_stop=True)