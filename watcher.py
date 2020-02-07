import intraserviceProvider, os
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
        self.acknowledged = []
        self.getTicketsFromFile()
        
    def addTicketToAcnowledged(self, ticketId):
        with open('data/chats/{0}.chat'.format(self.chatID), 'a+') as file:
            file.write('{0}\n'.format(ticketId))
        self.getTicketsFromFile()

    def getTicketsFromFile(self):
        if os.path.isfile('data/chats/{0}.chat'.format(self.chatID)) is True:
            content = open('data/chats/{0}.chat'.format(self.chatID),'r').read()
            if len(content) > 0:
                self.acknowledged = content.split('\n')

    def removeFile(self):
        if os.path.isfile('data/chats/{0}.chat'.format(self.chatID)) is True:
            os.remove('data/chats/{0}.chat'.format(self.chatID))
            self.acknoledged = []

# TODO: acknowledged cleanup

debugLog("Resetting variables...")
chatsForWatcher = {}
telebot = None
updateFunction = None

def initWatcher(bot, fun):
    global chatsForWatcher, telebot, updateFunction
    chatsForWatcher = {}
    telebot = bot
    updateFunction = fun
    if os.path.isfile('data/chats.list') is True:
        content = open('data/chats.list','r+').read()
        debugLog("Initializing watcher... chats to watch:")
        if len(content) > 0:
            for chatId in content.split('\n'):
                if chatId is "": continue           # skip an empty line at the end of the file
                chatsForWatcher[chatId] = chatToWatch(chatId)
                debugLog("\t{0}".format(chatId))
    timerWatcher = RepeatTimer(config.watcherChekoutInterval, sendUpdateFromWatcher)    
    timerWatcher.start()
    debugLog("Check timer is set to {0} seconds".format(config.watcherChekoutInterval))

def addChatToWatcher(chatId):
    debugLog("Adding new chat to watcher:")
    chatId = str(chatId)  
    with open('data/chats.list', 'a+') as file:
        file.seek(0)
        content = file.read()     
        ids = content.split('\n')
        if chatId not in ids:
            file.write('{0}\n'.format(chatId))
            chatsForWatcher[chatId] = chatToWatch(chatId)
            debugLog("\tchat {0} added.".format(chatId))
            return 'added'
        else:
            debugLog("\tchat {0} already added to watcher.".format(chatId))
            return 'already'

def removeChatFromWatcher(chatId):
    debugLog("Removing chat from watcher:")
    chatId = str(chatId)  
    file = open('data/chats.list', 'r')
    content = file.read()    
    ids = content.split('\n')
    if chatId in ids:
        stringToReplace = "{0}\n".format(chatId)
        content = content.replace(stringToReplace, "")        
        file = open('data/chats.list', 'w+')
        file.write(content)
        chatsForWatcher[chatId].removeFile()
        chatsForWatcher.pop(chatId, None)
        debugLog("\tchat {0} removed.".format(chatId))
        return 'removed'
    else:
        debugLog("\tchat {0} is not present in watcher list.".format(chatId))
        return 'wasnot'

def sendUpdateFromWatcher():
    debugLog("It's time to send watcher updates to: {0}".format(chatsForWatcher))
    watcherTickets = intraserviceProvider.getWatcher()
    if len(watcherTickets) > 0 and len(chatsForWatcher) > 0:
        #ticketIDs = [ticket.id for ticket in watcherTickets]        
        for chat in chatsForWatcher.items():
            debugLog("Filtering new tickets for chat {0}".format(chat[1].chatID))
            newTickets = filterNewTickets(chat[1].chatID, watcherTickets)            
            if len(newTickets) > 0:
                debugLog("New tickets: {0}".format(newTickets))
                updateFunction(chat[1].chatID, newTickets) 
            else:
                debugLog("\tNo new tickets for {}".format(chat[1].chatID))
    else:
        debugLog("\tWatcher is empty or no chats subscribed to updates...")
    

# filter already acknoledged tickets from received list
def filterNewTickets(chatID, tickets):
    newTickets = []
    for ticket in tickets:
        if str(ticket.id) not in chatsForWatcher[chatID].acknowledged:
            chatsForWatcher[chatID].addTicketToAcnowledged(ticket.id)
            newTickets.append(ticket)
    return newTickets
