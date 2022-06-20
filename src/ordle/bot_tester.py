import random
from game import Game
from bot import Bot
from typing import Type
from ui import print_inline_game, print_game_word, yellow, cyan


class BotTester:
    def __init__(self, game, bot_classes: list[Type[Bot]]):
        self.game = game
        self.bots = [bot() for bot in bot_classes]
        self.stats = dict((bot, []) for bot in self.bots)

    def run(self, n, seed=None, show=True):
        # generate words for testing
        if seed is not None:
            random.seed(seed)
        words = [
            self.game.wordlist[random.randint(0, len(self.game.wordlist) - 1)]
            for _ in range(n)
        ]

        # Play n games with all bots
        for word in words:
            if show:
                print_game_word(word)

            for bot in self.bots:
                name = bot.get_name()
                self.game.restart(word=word)
                bot.play(self.game)
                if self.game.state == Game.State.ACTIVE:
                    raise RuntimeError(f"Bot {name} did not complete the game.")

                if show:
                    print_inline_game(self.game, name)

                self.stats[bot].append(
                    BotTester.Result(
                        self.game.state == Game.State.WIN, self.game.attempts_used()
                    )
                )

    class Result:
        def __init__(self, win, attempts):
            self.win = win
            self.attempts = attempts

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
