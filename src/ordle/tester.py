import random
from game import Game
from bot import Bot
from typing import Type
from ui import print_inline_game, print_game_word, print_stats


class BotTester:
    class Result:
        def __init__(self, win, attempts):
            self.win = win
            self.attempts = attempts

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
                print_game_word(word, self.game.max_attempts)

            for bot in self.bots:
                name = bot.get_name()
                self.game._Game__restart(word=word)
                bot.play(self.game)
                if self.game.get_state() == Game.State.ACTIVE:
                    raise RuntimeError(f"Bot {name} did not complete the game.")

                if show:
                    print_inline_game(self.game, name)

                self.stats[bot].append(
                    BotTester.Result(
                        self.game.get_state() == Game.State.WIN,
                        self.game.attempts_used(),
                    )
                )
        self.summary()

    def summary(self):
        # calculate statistics
        games = len(next(iter(self.stats.values())))
        names = [bot.get_name() for bot in self.bots]
        wins = [sum(int(res.win) for res in self.stats[bot]) for bot in self.bots]
        attempts = [
            sum(int(res.attempts) for res in self.stats[bot] if res.win)
            for bot in self.bots
        ]
        rates = [n / games * 100 for n in wins]
        averages = [a / w if w > 0 else None for (a, w) in zip(attempts, wins)]

        # print
        print_stats(names, rates, averages, games, self.game)
