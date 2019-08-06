# -*- coding: UTF-8 -*-
import sqlite3

def createTablesIfNotExists():
    conn = sqlite3.connect('JackTeleBotUsers.db')
    cursor = conn.cursor()

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS [users] ('
        '[id] integer PRIMARY KEY NOT NULL, '
        '[name] string, '
        '[teleg_username] string,'
        '[intrId] integer;')

    conn.commit()
    conn.close()



def runQuery(query):
    conn = sqlite3.connect('JackTeleBotUsers.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result
