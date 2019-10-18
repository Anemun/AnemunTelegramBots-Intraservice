import intraserviceProvider
import config, botUserManager
from telebot import types

def returnTicketInfo(bot, call):
    # PARTIALLY IMPLEMENTED IN CURRENT BUILD
    ticketId = call.data.split('_')[1]
    ticket = intraserviceProvider.getTicketById(ticketId)
    #keyboard = types.InlineKeyboardMarkup()
    #buttonAddExec = types.InlineKeyboardButton(text="Добавить исполнителя", callback_data="addEx_"+ str(ticket.id))
    #keyboard.add(buttonAddExec)
    if len(ticket.executors) > 0:
        executors = ""
        for i in range(0, len(ticket.executors)):
            if len(ticket.executors)-1 == i:  # if i is the last element, we do not want the comma
                executors += "{0}".format(ticket.executors[i])
            else:
                executors += "{0}, ".format(ticket.executors[i])
        # bot.send_message(chat_id=call.message.chat.id, text="№: {0}\nСоздатель: {1}\nНазвание: {2}\nИсполнители: {3}"
        #                                              .format(ticket.id, ticket.creatorName, ticket.title, executors), 
        #                                                                                        reply_markup=keyboard)
        bot.send_message(chat_id=call.message.chat.id, text="№: {0}\nСоздатель: {1}\nНазвание: {2}\nОписание: {3}\nИсполнители: {4}"
                                                     .format(ticket.id, ticket.creatorName, ticket.title, ticket.description, executors))
    else:
        # bot.send_message(chat_id=call.message.chat.id, text="№: {0}\nСоздатель: {1}\nНазвание: {2}"
        #                                       .format(ticket.id, ticket.creatorName, ticket.title),
        #                                                                      reply_markup=keyboard)
        bot.send_message(chat_id=call.message.chat.id, text="№: {0}\nСоздатель: {1}\nНазвание: {2}\nОписание: {3}"
                                              .format(ticket.id, ticket.creatorName, ticket.title, ticket.description))

# # TODO:
# def createNewTicket(bot, call):
#     ticketId = call.data.split('_')[1]
#     ticket = intraserviceProvider.getTicketById(ticketId)
#     bot.send_message(chat_id=call.message.chat.id, text="№: {0}\nСоздатель: {1}\nНазвание: {2}".format(ticket.id, ticket.creatorName, ticket.title))

# def addExecutor(bot, call):
#     ticketId = call.data.split('_')[1]
#     ticket = intraserviceProvider.getTicketById(ticketId)
#     keyboard = types.InlineKeyboardMarkup()
#     botIdList = botUserManager.getIdsList()
    
#     for i in range(0, len(botIdList)):
#         username = intraserviceProvider.getExecutorNameById(botIdList[i])
#         button = types.InlineKeyboardButton(
#             text=str(username), 
#             callback_data="ExAdded_"+ str(ticket.id)+"_"+str(username))
#         keyboard.add(button) 



#     #TODO: Add Executor to intraservice
#     executors = ""
#     if len(ticket.executors) > 0:
        
#         for i in range(0, len(ticket.executors)):
#             if len(ticket.executors)-1 == i:  # if i is the last element, we do not want the comma
#                 executors += "{0}".format(ticket.executors[i])
#             else:
#                 executors += "{0}, ".format(ticket.executors[i])
    
#     bot.edit_message_text(chat_id=call.message.chat.id, 
#                             message_id=call.message.message_id, 
#                             text="№: {0}\nСоздатель: {1}\nНазвание: {2}\nИсполнители: {3}"
#                                                      .format(ticket.id, ticket.creatorName, ticket.title, executors), 
#                                                                                                reply_markup=keyboard)
        