import config

activeUsers = []

def loadUsers():
    content = open(config.userListFile,'r+').read()
    lines = content.split('\n')
    for line in lines:
        user = line.split(':')
        activeUsers.append(user[0])
    if len(activeUsers) == 0:
        raise "Users must be configured!"

def getUserList():
    content = open(config.userListFile,'r+').read()
    lines = content.split('\n')
    users = []
    for line in lines:
        l = line.split(':')
        users.append(l[0])
    if len(users) > 0:
        return users
    if len(users) == 0:
        raise "Users must be configured!"

def getIdsList():
    content = open(config.userListFile,'r+').read()
    lines = content.split('\n')
    ids = []
    for line in lines:
        l = line.split(':')
        ids.append(l[1])
    if len(ids) > 0:
        return ids
    if len(ids) == 0:
        raise "Users must be configured!"