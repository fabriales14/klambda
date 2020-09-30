from interfaces import command

class CLICommand(command.ICommand):

    parameter = "" # the parameter setted when the command will be executed

    def __init__(self, pAction, pHelp) -> None:
        """
        Complex commands can accept one or several receiver objects along with
        any context data via the constructor.
        """
        self.action = pAction # the action that the command will execute
        self.help = pHelp # the help related to the usage of the command in the CLI

    # method from the command abstract class
    def execute(self) -> None:
        """
        Commands can delegate to any methods of a receiver.
        """

        self.action(self.parameter)
        return self