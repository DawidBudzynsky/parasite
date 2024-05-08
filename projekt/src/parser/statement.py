from abc import ABC, abstractmethod


class Statement(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitator):
        pass
