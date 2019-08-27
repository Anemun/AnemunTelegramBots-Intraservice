import intraserviceProvider, os
import Ticket
from threading import Timer

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
        if len(content) > 0:
            for chatId in content.split('\n'):
                if chatId is "": continue           # skip an empty line at the end of the file
                chatsForWatcher[chatId] = chatToWatch(chatId)
    timerWatcher = RepeatTimer(10, sendUpdateFromWatcher)    
    timerWatcher.start()

def addChatToWatcher(chatId):
    chatId = str(chatId)  
    with open('data/chats.list', 'a+') as file:
        file.seek(0)
        content = file.read()     
        ids = content.split('\n')
        if chatId not in ids:
            file.write('{0}\n'.format(chatId))
            chatsForWatcher[chatId] = chatToWatch(chatId)
            return 'added'
        else:
            return 'already'

def removeChatFromWatcher(chatId):
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
        return 'removed'
    else:
        return 'wasnot'

def sendUpdateFromWatcher():
    watcherTickets = intraserviceProvider.getWatcher()
    if len(watcherTickets) > 0:
        ticketIDs = [ticket.id for ticket in watcherTickets]
        for chat in chatsForWatcher:
            newTickets = filterNewTickets(chat, watcherTickets)
            if len(newTickets) > 0:
                updateFunction(chat, newTickets)
                pass
    # check for tickets in watcher list
    # for each chatID check is any of tickets is new
    # if it it, form a list and send it.
    pass

# filter already acknoledged tickets from received list
def filterNewTickets(chatID, tickets):
    newTickets = []
    for ticket in tickets:
        if str(ticket.id) not in chatsForWatcher[chatID].acknowledged:
            chatsForWatcher[chatID].addTicketToAcnowledged(ticket.id)
            newTickets.append(ticket)
    return newTickets