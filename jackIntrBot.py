import telebot, config
import argparse, os
import intraserviceProvider, watcher, lambdaHandlers, databaseProvider
from telebot import types
from tools import debugLog

version = "0.5.1"

parser=argparse.ArgumentParser()
parser.add_argument('--botToken', help='telegram bot token')
parser.add_argument('--site', help='intraservice address')
parser.add_argument('--siteLogin', help='intraservice login')
parser.add_argument('--sitePass', help='intraservice password')
parser.add_argument('--filterId', help='filter id in intraservice for watcher')
parser.add_argument('--interval', help='watcher interval between checks is seconds')
parser.add_argument('--users', help='telegram usernames users divided by comma')
args=parser.parse_args()
botToken = args.botToken

bot = telebot.TeleBot(botToken)
config.site = args.site
login = args.siteLogin
password = args.sitePass
config.filterId = args.filterId
config.watcherChekoutInterval = int(args.interval)
intraserviceProvider.login = login
intraserviceProvider.password = password
intraserviceProvider.setBaseUrl(config.site)

databaseProvider.createTablesIfNotExists()
for user in args.users.split(','):
    databaseProvider.addNewUser(user)

debugLog("Бот для Интрасервиса запущен (вер. {0})".format(version))

@bot.message_handler(commands=["start"])
def command_start(message):
    if databaseProvider.authUser(message.from_user.username) is True:
        bot.send_message(message.chat.id, "Вы можете пользоваться ботом. Попробуйте следующие команды:\n/fresh\n/watch\n/stop")
    else:
        bot.send_message(message.chat.id, "Использование данного бота не авторизовано. Обратитесь к администратору.")

@bot.message_handler(commands=["fresh"])
def command_fresh(message):
    tickets = {}
    if databaseProvider.authUser(message.from_user.username) is False:
        return
    tickets, err = intraserviceProvider.getWatcher()
    if tickets is None:
        bot.send_message(chat_id=message.chat.id, text="Ошибка подключения к Intraservice: " + str(err) + ". Обратитесь к администратору.")
        return
    keyboard = types.InlineKeyboardMarkup()
    for ticket in tickets:
        button = types.InlineKeyboardButton(text="[{0}] {1}".format(ticket.id, ticket.title), callback_data="ticket_"+ str(ticket.id))
        keyboard.add(button)
    bot.send_message(chat_id=message.chat.id, text="Заявок в диспетчере: " + str(len(tickets)),reply_markup=keyboard)

@bot.message_handler(commands=["watch"])
def command_watch(message):
    if databaseProvider.authUser(message.from_user.username) is False:
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
    if databaseProvider.authUser(message.from_user.username) is False:
        return
    result = watcher.removeChatFromWatcher(message.chat.id)
    if result == 'removed':
        bot.send_message(chat_id=message.chat.id, text="Данный чат более не будет получать обновлений диспетчера")
    if result == 'wasnot':
        bot.send_message(chat_id=message.chat.id, text="Данный чат не подписан на обновления диспетчера")

@bot.message_handler(commands=["users"])
def command_users(message):
    if databaseProvider.authUser(message.from_user.username) is False:
        return
    users = databaseProvider.getUsers()
    bot.send_message(chat_id=message.chat.id, text="Пользователи с доступом к боту:\n{0}".format('\n'.join(users)))

def sendWatcherUpdates(chatId, tickets):
    if len(tickets) > 0:
        debugLog("New tickets in watcher ({0}), sending updates...".format(len(tickets)))
        for ticket in tickets:
            bot.send_message(
                chat_id=chatId, 
                parse_mode="markdown", 
                text="*№:* [{0}](https://{5}.intraservice.ru/Task/View/{0})\n*Создатель:* {1} ({2})\n*Название:* {3}\n*Описание:* {4}"
                    .format(ticket.id, ticket.creatorName, ticket.creatorCompanyName, ticket.title, ticket.description, config.site))


watcher.initWatcher(bot, sendWatcherUpdates)

# Catch calldata
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    callType = call.data.split('_')[0]
    if callType == "ticket":
        lambdaHandlers.returnTicketInfo(bot,call)
        
if __name__ == '__main__':
    bot.polling(none_stop=False, interval=5, timeout=60)
    