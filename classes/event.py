import uuid

class Event():

    def __init__(self, pProject, pAuthor, pDate, pUser, pAction, pModule):
        self.id = str(uuid.uuid1())
        self.project = pProject
        self.author = pAuthor
        self.date = pDate
        self.user = pUser
        self.action = pAction
        self.on_module = pModule
