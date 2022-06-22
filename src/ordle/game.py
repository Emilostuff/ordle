import random
from letter import Letter
from enum import Enum
from data import get_words


class Game:
    """A representation of an ORDLE game

    Public attributes:
    - wordlist: all valid words
    - alphabet: the accepted alphabet
    - max_attempts: how many guesses can be made
    - word_length: the length of the secret word
    - guesses: a list of the previous guesses
        (each as a list of Letter objects)
    - letters: the current knowledge about each letter
        (a dict of Letter objects accessed by its associated character)
    """

    class State(Enum):
        """The different game states"""

        ACTIVE = 0
        WIN = 1
        DEFEAT = 2

    def __init__(self, word_length, alphabet, max_attempts):
        self.wordlist = get_words(length=word_length, alphabet=alphabet)
        self.alphabet = alphabet.upper()
        self.max_attempts = max_attempts
        self.word_length = word_length
        self.__restart()

    def __restart(self, word=None):
        # Public state
        self.guesses = []
        self.letters = dict()
        for c in self.alphabet:
            self.letters[c] = Letter(c)

        # Private state
        self.__state = Game.State.ACTIVE
        self.__attempts = 0
        if word is None:
            self.__word = random.choice(self.wordlist)
        elif word in self.wordlist:
            word = word.upper()
            self.__word = word
        else:
            raise ValueError("Game restarted with invalid word.")

    def __parse_guess(self, guess):
        guess_letters = []
        for (i, c) in enumerate(guess):
            # evaluate guess letter
            let = Letter(c)
            if c == self.__word[i]:
                let.state = Letter.State.CORRECT
            elif c in self.__word:
                let.state = Letter.State.INCLUDED
            else:
                let.state = Letter.State.EXCLUDED
            guess_letters.append(let)

            # update overall letter status
            self.letters[let.value].update_state(let)

        self.guesses.append(guess_letters)

    def make_guess(self, guess: str):
        """Submit a guess to the current game

        Returns:
            bool: whether or not the guess was valid (and hence accepted)
        """
        guess = guess.upper()
        if guess not in self.wordlist:
            return False
        elif self.__state == Game.State.ACTIVE:
            self.__attempts += 1
            self.__parse_guess(guess)

            if guess == self.__word:
                self.__state = Game.State.WIN
            elif self.attempts_left() < 1:
                self.__state = Game.State.DEFEAT
            return True
        else:
            return False

    def last_guess(self):
        """Get the last guess

        Returns:
            list[Letter]: last guess as a list of Letters
        """
        return self.guesses[-1] if len(self.guesses) > 0 else []

    def attempts_used(self):
        """Get the number of attemps used so far

        Returns:
            int: number of attempts
        """
        return self.__attempts

    def attempts_left(self):
        """Get the amount of attempts left in the game

        Returns:
            int: number of attempts left
        """
        return self.max_attempts - self.__attempts

    def get_state(self):
        return self.__state

    def get_answer(self):
        """Reveal the answer if the game is finished

        Returns:
            str: the secret word
        """
        if self.__state == Game.State.ACTIVE:
            raise RuntimeError("Can't reveal answer while game is in progress")
        else:
            return self.__word
