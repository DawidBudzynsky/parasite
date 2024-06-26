from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def __init__(self, position):
        self.position = position

    @abstractmethod
    def accept(self, visitator):
        pass
