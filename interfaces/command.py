from abc import ABC, abstractmethod

class ICommand(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    def execute(self) -> None:
        pass