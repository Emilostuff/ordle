from abc import abstractmethod
from game import Game


class Bot:
    """The base class for every bot"""

    @abstractmethod
    def play(self, game: Game):
        """A function that plays the given game object until completion

        Args:
            game (Game): the game to be played
        """
        pass

    def get_name(self):
        """Get the name of the bot.
        Override this if you want a name that is different from the class name.

        Returns:
            str: name
        """
        return self.__class__.__name__
