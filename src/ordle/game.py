import random
from letter import Letter
from enum import Enum
from data import get_words


class Game:
    class State(Enum):
        ACTIVE = 0
        WIN = 1
        DEFEAT = 2

    def __init__(self, word_length, alphabet, max_attempts):
        # Static setup
        self.wordlist = get_words(length=word_length, alphabet=alphabet)
        self.alphabet = alphabet.upper()
        self.max_attempts = max_attempts

        # Public state
        self.state = Game.State.ACTIVE
        self.guesses = []
        self.letters = dict()
        for c in alphabet:
            self.letters[c] = Letter(c)

        # Private state
        self.__attempts = 0
        self.__word = random.choice(self.wordlist)

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

    def restart(self):
        # Public state
        self.state = Game.State.ACTIVE
        self.guesses = []
        for c in self.alphabet:
            self.letters[c].state = Letter.State.UNKNOWN

        # Private state
        self.__attempts = 0
        self.__word = random.choice(self.wordlist)

    def make_guess(self, guess):
        guess = guess.upper()
        if guess not in self.wordlist:
            return False
        elif self.state == Game.State.ACTIVE:
            self.__attempts += 1
            self.__parse_guess(guess)

            if guess == self.__word:
                self.state = Game.State.WIN
            elif self.__attempts >= self.max_attempts:
                self.state = Game.State.DEFEAT
            return True
        else:
            return False

    def last_guess(self):
        return self.guesses[-1] if len(self.guesses) > 0 else []

    def attempts_used(self):
        return self.__attempts

    def get_answer(self):
        if self.state == Game.State.ACTIVE:
            raise RuntimeError("Can't reveal answer while game is in progress")
        else:
            return self.__word
