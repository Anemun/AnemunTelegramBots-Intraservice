import intraserviceProvider, databaseProvider, os
import Ticket
import config
from threading import Timer
from tools import debugLog

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class chatToWatch:
    def __init__(self, newChatID):
        self.chatID = newChatID
        
    def addTicketToAcnowledged(self, ticketId):
        databaseProvider.recordTicket(self.chatID, ticketId)

debugLog("Resetting variables...")
chatsForWatcher = {}
telebot = None
updateFunction = None

def initWatcher(bot, fun):
    global chatsForWatcher, telebot, updateFunction
    chatsForWatcher = {}
    telebot = bot
    updateFunction = fun
    debugLog("Initializing watcher... chats to watch:")
    chats = databaseProvider.getChatsToWatch()
    if len(chats) > 0:
        for chatId in chats:
            chatsForWatcher[chatId] = chatToWatch(chatId)
            debugLog("\t{0}".format(chatId))
    timerWatcher = RepeatTimer(config.watcherChekoutInterval, sendUpdateFromWatcher)    
    timerWatcher.start()
    debugLog("Check timer is set to {0} seconds".format(config.watcherChekoutInterval))

def addChatToWatcher(chatId):
    debugLog("Adding new chat to watcher:")
    chatId = str(chatId)  
    return databaseProvider.addChatToWatch(chatId)

def removeChatFromWatcher(chatId):    
    debugLog("Removing chat from watcher:")
    chatId = str(chatId)  
    return databaseProvider.removeChatToWatch(chatId)

def sendUpdateFromWatcher():
    chats = databaseProvider.getChatsToWatch()
    debugLog("It's time to send watcher updates to: {0}".format(chats))
    watcherTickets = intraserviceProvider.getWatcher()
    if watcherTickets is None:
        return
    if len(watcherTickets) > 0 and len(chats) > 0:   
        for chat in chats:
            debugLog("Filtering new tickets for chat {0}".format(chat))
            newTickets = filterNewTickets(chat, watcherTickets)            
            if len(newTickets) > 0:
                ticketIDs = list(map(lambda x: x.id, newTickets))
                debugLog("New tickets: {0}".format(",".join([str(tid) for tid in ticketIDs])))
                updateFunction(chat, newTickets) 
            else:
                debugLog("\tNo new tickets for {}".format(chat))
    else:
        debugLog("\tWatcher is empty or no chats subscribed to updates...")    

# filter already acknoledged tickets from received list
def filterNewTickets(chatID, tickets):
    oldTickets = databaseProvider.getTicketsForChat(chatID)
    newTickets = []
    for ticket in tickets[0]:
        if ticket.id not in oldTickets:
            databaseProvider.recordTicket(chatID, str(ticket.id))
            newTickets.append(ticket)
    return newTickets
