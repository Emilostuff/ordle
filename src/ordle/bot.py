from abc import abstractmethod
from game import Game


class Bot:
    @abstractmethod
    def play(self, game: Game):
        pass

    def get_name(self):
        return self.__class__.__name__
