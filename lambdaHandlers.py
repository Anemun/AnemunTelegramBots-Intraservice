import intraserviceProvider
import config
from telebot import types

def returnTicketInfo(bot, call):
    ticketId = call.data.split('_')[1]
    ticket = intraserviceProvider.getTicketById(ticketId)
    if len(ticket.executors) > 0:
        executors = ""
        for i in range(0, len(ticket.executors)):
            if len(ticket.executors)-1 == i:  # if i is the last element, we do not want the comma
                executors += "{0}".format(ticket.executors[i])
            else:
                executors += "{0}, ".format(ticket.executors[i])
        bot.send_message(chat_id=call.message.chat.id, parse_mode="markdown", text="*№:* [{0}](https://jack-it.intraservice.ru/Task/View/{0})\n*Создатель:* {1} ({2})\n*Название:* {3}\n*Описание:* {4}\n*Исполнители:* {5}"
                                                     .format(ticket.id, ticket.creatorName, ticket.creatorCompanyName, ticket.title, ticket.description, executors))
    else:
        bot.send_message(chat_id=call.message.chat.id, parse_mode="markdown", text="*№:* [{0}](https://jack-it.intraservice.ru/Task/View/{0})\n*Создатель:* {1} ({2})\n*Название:* {3}\n*Описание:* {4}"
                                              .format(ticket.id, ticket.creatorName, ticket.creatorCompanyName, ticket.title, ticket.description))    