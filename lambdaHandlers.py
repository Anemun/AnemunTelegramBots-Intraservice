import intraserviceProvider
import config
from telebot import types

def returnTicketInfo(bot, call):
    ticketId = call.data.split('_')[1]
    ticket = intraserviceProvider.getTicketById(ticketId)
    bot.send_message(
        chat_id=call.message.chat.id, 
        parse_mode="markdown", 
        text="*№:* [{0}](https://{5}.intraservice.ru/Task/View/{0})\n*Создатель:* {1} ({2})\n*Название:* {3}\n*Описание:* {4}"
            .format(ticket.id, ticket.creatorName, ticket.creatorCompanyName, ticket.title, ticket.description, config.site))    