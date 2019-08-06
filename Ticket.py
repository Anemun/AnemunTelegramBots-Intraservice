class Ticket:
    def __init__(self, 
    ticketId, status, title, 
    creatorName, creatorCompanyName, creationDate, 
    description, dueDate, executors):
        """
        :param ticketId:
        :param status: must be Id
        
        """
        self.id = ticketId
        self.status = status
        self.title = title
        self.creatorName = creatorName
        self.creatorCompanyName = creatorCompanyName
        self.creationDate = creationDate
        self.description = description
        self.dueDate = dueDate
        self.executors = executors