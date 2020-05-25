import requests
import config
import Ticket
import sys
from tools import debugLog

baseUrl = ""
companies = {}
statuses = {}
executors = {}

login = ""
password = ""

def setBaseUrl(site):
    global baseUrl
    baseUrl = "https://{0}.intraservice.ru/api/".format(site)

def getCompanyNameByUserName(name):
    if name in companies:
        return companies[name]
    else:
        url = baseUrl + "user?name=" + name
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(login, password)).json()
        companyName = r['Users'][0]['Companyname']
        companies[name] = companyName
        return companies[name]

def getStatusNameById(statusId):
    if statusId in statuses:
        return statuses[statusId]
    else:
        url = baseUrl + "taskstatus"
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(login, password)).json()
        for status in r:
            if status['Id'] == statusId:
                statusName = status['Name']
        statuses[statusId] = statusName
        return statuses[statusId]

def getExecutorNameById(executorId):
    if executorId == '':
        return None
    if executorId in executors:
        return executors[executorId]
    else:
        url = baseUrl + "user?id=" + executorId
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(login, password)).json()
        executorName = r['Name']
        executors[executorId] = executorName
        return executors[executorId]

def parseJSONintoTicketClass(jsonData):
    tickets = []    
    for task in jsonData['Tasks']:
        executorsNames = []
        for id in task['ExecutorIds'].split(','):
            id = str.strip(id)
            executorsNames.append(getExecutorNameById(id))

        ticket = Ticket.Ticket(
            ticketId=task['Id'], 
            status=getStatusNameById(task['StatusId']), 
            title=task['Name'], 
            creatorName=task['Creator'], 
            creatorCompanyName=getCompanyNameByUserName(task['Creator']), 
            creationDate=task['Created'], 
            description=task['Description'], 
            dueDate=task['Deadline'],
            executors=executorsNames)        
        tickets.append(ticket)

    return tickets

def parseJSONintoTicketClass_singleTask(jsonData):
    task = jsonData['Task']
    executorsNames = []
    if task['ExecutorIds'] is not None:
        for id in task['ExecutorIds'].split(','):
            id = str.strip(id)
            executorsNames.append(getExecutorNameById(id))

    ticket = Ticket.Ticket(
            ticketId=task['Id'], 
            status=getStatusNameById(task['StatusId']), 
            title=task['Name'], 
            creatorName=task['Creator'], 
            creatorCompanyName=getCompanyNameByUserName(task['Creator']), 
            creationDate=task['Created'], 
            description=task['Description'], 
            dueDate=task['Deadline'],
            executors=executorsNames)
    return ticket

def getIntrIdByUsername(targetUsername):    
    content = open(config.userListFile,'r+').read()
    lines = content.split('\n')
    for line in lines:
        l = line.split(':')
        if l[0] == targetUsername:
            return l[1]
    return None

def getIntrUsernameById(targetId):    
    content = open(config.userListFile,'r+').read()
    lines = content.split('\n')
    for line in lines:
        l = line.split(':')
        if l[1] == targetId:
            return l[0]
    return None

def auth(username):    
    if getIntrIdByUsername(username) is not None:
        print("Telegram user {0} demanded auth: success".format(username))
        return True
    else:
        print("Telegram user {0} demanded auth: failure".format(username))
        return False

def getWatcher():    
    for i in range(0, 5):
        try:
            debugLog("Getting watcher tickets from intraservice (attempt {} of 5)...".format(i+1))
            url = baseUrl + "task?filterid=636"
            r = requests.get(url, auth=requests.auth.HTTPBasicAuth(login, password)).json()
            tickets = parseJSONintoTicketClass(r)
            debugLog("\tdone.\n{0}".format(tickets))
        except:         
            debugLog("error: {0}".format(sys.exc_info()[0]))
            continue
        break
    return tickets

def getTicketById(id):
    url = baseUrl + "task/" + str(id)
    r = requests.get(url, auth=requests.auth.HTTPBasicAuth(login, password)).json()
    ticket = parseJSONintoTicketClass_singleTask(r)
    return ticket

def createNewTicket():
    pass
