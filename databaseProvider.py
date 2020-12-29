# -*- coding: UTF-8 -*-
import sqlite3
import config
from tools import debugLog

def createTablesIfNotExists():
    conn = sqlite3.connect(config.dbFilename)
    cursor = conn.cursor()

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS [users] ('
        '[id] integer PRIMARY KEY NOT NULL, '
        '[telegramUsername] string);')

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS [chats] ('
        '[chatId] string PRIMARY KEY NOT NULL);')

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS [tickets] ('
        '[chatId] string, '
        '[ticketId] integer);')

    conn.commit()
    conn.close()

def authUser(telegramUsername):
    userExist = runQuery("SELECT EXISTS (SELECT 1 FROM users WHERE telegramUsername = '{0}' LIMIT 1);".format(telegramUsername))[0][0]
    if userExist == 1:
        debugLog("User {0} demanded auth - ACCEPTED".format(telegramUsername))
        return True
    if userExist == 0:
        debugLog("User {0} demanded auth - DENIED".format(telegramUsername))
        return False

def addNewUser(telegramUsername, name=""):
    userExist = runQuery("SELECT EXISTS (SELECT 1 FROM users WHERE telegramUsername = '{0}' LIMIT 1);".format(telegramUsername))[0][0]
    if userExist == 0:          # 0 - user not exists, 1 - user exists
        runQuery("INSERT INTO users (telegramUsername) VALUES ('{0}')".format(telegramUsername))
        debugLog("new user {0} ({1})".format(name, telegramUsername))
        return "ok"
    elif userExist == 1:
        return "exists"

def getUsers():
    result = runQuery("SELECT telegramUsername FROM users")
    users = list(map(lambda x: x[0], result))
    return users

def getTicketsForChat(chatId):
    result = runQuery("SELECT ticketId FROM tickets WHERE chatId = '{0}'".format(chatId))
    tickets = list(map(lambda x: x[0], result))
    return tickets

def addChatToWatch(chatId):
    chatExist = runQuery("SELECT EXISTS (SELECT 1 FROM chats WHERE chatId = '{0}' LIMIT 1);".format(chatId))[0][0]
    if chatExist == 0:          # 0 - not exist, 1 - exist 
        runQuery("INSERT OR IGNORE INTO chats (chatId) VALUES ('{0}')".format(chatId))
        debugLog("\tchat {0} added.".format(chatId))
        return "added"
    elif chatExist == 1:
        debugLog("\tchat {0} already added to watcher.".format(chatId))
        return "already"

def removeChatToWatch(chatId):
    chatExist = runQuery("SELECT EXISTS (SELECT 1 FROM chats WHERE chatId = '{0}' LIMIT 1);".format(chatId))[0][0]
    if chatExist == 1:          # 0 - not exist, 1 - exist 
        runQuery("DELETE FROM chats WHERE chatId = '{0}'".format(chatId))
        runQuery("DELETE FROM tickets WHERE chatId = '{0}'".format(chatId))
        debugLog("\tchat {0} removed.".format(chatId))
        return 'removed'
    elif chatExist == 0:
        debugLog("\tchat {0} is not present in watcher list.".format(chatId))
        return 'wasnot'      

def getChatsToWatch():
    result = runQuery("SELECT chatId FROM chats")
    chats = list(map(lambda x: x[0], result))
    return chats

def recordTicket(chatId, ticketId):
    ticketForChatExist = runQuery("SELECT EXISTS (SELECT 1 FROM tickets WHERE chatId = '{0}' AND ticketId = '{1}' LIMIT 1);".format(chatId, ticketId))[0][0]
    if ticketForChatExist == 0:          # 0 - not exist, 1 - exist
        runQuery("INSERT INTO tickets (chatId, ticketId) VALUES ('{0}', '{1}')".format(chatId, ticketId))    

def runQuery(query):
    conn = sqlite3.connect('JackTeleBotUsers.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result
