import telebot
import argparse, sys, os
import intraserviceProvider, watcher, recognizer
import soundfile as sf
from telebot import types

version = "0.2.1"

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

print("Intraservice bot started (ver. {0})".format(version))

try:
    os.makedirs('./data/chats')
except OSError:
    pass
if os.path.isfile('data/users.list') is False: 
    open('data/users.list','w+')



@bot.message_handler(commands=["start"])
def command_start(message):
    if intraserviceProvider.auth(message.from_user.username) is True:
        bot.send_message(message.chat.id, "Вы можете пользоваться ботом. Попробуйте следующие команды:\n/fresh\n/watch\n/stop")
    else:
        bot.send_message(message.chat.id, "Использование данного бота не авторизовано. Обратитесь к администратору.")

@bot.message_handler(commands=["fresh"])
def command_fresh(message):
    if intraserviceProvider.auth(message.from_user.username) is False:
        return
    tickets = intraserviceProvider.getWatcher()
    keyboard = types.InlineKeyboardMarkup()
    for ticket in tickets:
        button = types.InlineKeyboardButton(text=ticket.title, callback_data="ticket_"+ str(ticket.id))
        keyboard.add(button)
    bot.send_message(chat_id=message.chat.id, text="Диспетчер: " + str(len(tickets)) + " заявок",reply_markup=keyboard)

@bot.message_handler(commands=["watch"])
def command_watch(message):
    if intraserviceProvider.auth(message.from_user.username) is False:
        return
    result = watcher.addChatToWatcher(message.chat.id)        
    if result == 'added':
        bot.send_message(chat_id=message.chat.id, text="Данный чат теперь подписан на обновления диспетчера")
        return
    if result == 'already':
        bot.send_message(chat_id=message.chat.id, text="Данный чат уже имеет подписку на обновления диспетчера")
        return

@bot.message_handler(commands=["stop"])
def command_stop(message):
    if intraserviceProvider.auth(message.from_user.username) is False:
        return
    result = watcher.removeChatFromWatcher(message.chat.id)
    if result == 'removed':
        bot.send_message(chat_id=message.chat.id, text="Данный чат более не будет получать обновлений диспетчера")
    if result == 'wasnot':
        bot.send_message(chat_id=message.chat.id, text="Данный чат не подписан на обновления диспетчера")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.split('_')[0] == "ticket":
        ticketId = call.data.split('_')[1]
    ticket = intraserviceProvider.getTicketById(ticketId)
    bot.send_message(chat_id=call.message.chat.id, text="№: {0}\nСоздатель: {1}\nНазвание: {2}".format(ticket.id, ticket.creatorName, ticket.title))

@bot.message_handler(content_types=['voice'])
def newTicketFromAudio(message):
    oggFilePath = './data/voices/{0}.ogg'.format(message.voice.file_id)
    wavFilePath = './data/voices/{0}.wav'.format(message.voice.file_id)

    # download file from Telegram
    file_onserver = bot.get_file(message.voice.file_id)
    file_downloaded=bot.download_file(file_onserver.file_path)
    with open(oggFilePath, 'wb') as newfile:
        newfile.write(file_downloaded)

    # convert from ogg to wav (apt-get install ffmpeg for that!)
    import subprocess
    process = subprocess.run(['ffmpeg', '-i', oggFilePath, wavFilePath])
    if process.returncode != 0:
        raise Exception("Something went wrong")
    os.remove(oggFilePath)
    
    # TEMP. send recognition result back to chat (should create new ticket with recognized text)
    result = recognizer.recognize(wavFilePath)    
    os.remove(wavFilePath)    
    bot.send_message(chat_id=message.chat.id, text=result)

@bot.message_handler()
def newTicketFromInput(message):
    bot.send_message(chat_id=message.chat.id, text=message.text)

def sendWatcherUpdates(chatId, tickets):
    keyboard = types.InlineKeyboardMarkup()
    for ticket in tickets:
        button = types.InlineKeyboardButton(text=ticket.title, callback_data="ticket_"+ str(ticket.id))
        keyboard.add(button)
    bot.send_message(chat_id=chatId, text="В диспетчере появилось новых заявок: {0}".format(len(tickets)),reply_markup=keyboard)

watcher.initWatcher(bot, sendWatcherUpdates)

if __name__ == '__main__':
    bot.polling(none_stop=True)