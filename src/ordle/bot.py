from abc import abstractmethod
from game import Game
from ui import print_guess, red, cyan, yellow
import random


class Bot:
    class Result:
        def __init__(self, win, attempts):
            self.win = win
            self.attempts = attempts

    def __init__(self, game):
        self.game = game
        self.results = []

    @abstractmethod
    def play(self):
        pass

    def test(self, n, seed=None, show=True):
        # seed
        if seed is not None:
            random.seed(seed)
        seeds = [random.randint(0, len(self.game.wordlist) - 1)
                 for _ in range(n)]

        # play n different games
        for seed in seeds:
            # setup
            self.game.restart(seed=seed)
            # play
            self.play()
            # evaluate
            win = self.game.state == Game.State.WIN
            attempts = self.game.attempts_used()
            self.results.append(Bot.Result(win, attempts))
            # show game
            if show:
                for i in range(self.game.attempts_used()):
                    print_guess(self.game, number=i)
                    print("  ", end="")
                print(red("[DEFEAT]") if not win else "")

    def print_stats(self):
        games = len(self.results)
        wins = sum(int(res.win) for res in self.results)
        attempts = sum(int(res.attempts) for res in self.results if res.win)
        rate = wins / games * 100
        avr = attempts / wins
        print()
        print(cyan("SUMMARY"))
        print("Success rate:", yellow(f"{rate:.1f}%"))
        print("Average attempts", yellow(f"{avr:.2f}"))
        print()
