import abc
from services import logger

class BaseModule():
    # parent class of the modules of each AWS service

    def __init__(self, pClient, pName, pDescription, pReader):
        
        self.client = pClient
        self.name = pName
        self.description = pDescription
        self.commands = {} # dictionary containing all the commands of the module
        self.reader = pReader

    def register(self, pCommandName, pCommand):
        # for register a command by name
        self.commands[pCommandName] = pCommand

    def execute(self, pCommandName, pParameter):
        # executes a commands by name and set the parameter
        if pCommandName in self.commands.keys():
            self.commands[pCommandName].parameter = pParameter
            self.commands[pCommandName].execute()
        else:
            logger.error("Command [{pCommandName}] not recognised")

    @abc.abstractmethod
    def register_commands(self):
        raise NotImplementedError("Please Implement this method")