from game import Game
from ui import print_guess, red, cyan, yellow
import bot_utils


class Result:
    def __init__(self, win, attempts):
        self.win = win
        self.attempts = attempts


class Bot:
    def __init__(self, game):
        self.game = game
        self.results = []

    def play(self, n, first_guesses, show=True):
        # check first guess
        first_guess = first_guesses[self.game.word_length]
        if len(first_guess) != self.game.word_length:
            raise ValueError("First guess was the wrong length!")
        if first_guess not in self.game.wordlist:
            raise ValueError("First guess is not valid!")

        # play n different games
        for _ in range(n):
            # setup game
            self.game.restart()
            candidates = self.game.wordlist
            info = bot_utils.Info(game)
            guess = first_guess

            # Game loop
            for _ in range(self.game.max_attempts):
                # make guess and check win
                game.make_guess(guess)

                # print guess
                if show:
                    print_guess(self.game)
                    print("  ", end="")
                info.guesses.append(guess)

                # check for game over
                if game.state != Game.State.ACTIVE:
                    win = game.state == Game.State.WIN
                    attempts = self.game.attempts_used()
                    self.results.append(Result(win, attempts))
                    if show:
                        print(red("[DEFEAT]") if not win else "")
                    break

                # parse result and filter wordlist
                bot_utils.parse(self.game, info)
                candidates = bot_utils.filter(candidates, info)

                # pick a new guess
                guess = bot_utils.pick(candidates, info)

    def print_stats(self):
        games = len(self.results)
        attempts = 0
        wins = 0

        for res in self.results:
            if res.win:
                wins += 1
                attempts += res.attempts

        rate = wins / games * 100
        avr = attempts / wins

        print()
        print(cyan("SUMMARY"))
        print("Success rate:", yellow(f"{rate:.1f}%"))
        print("Average attempts", yellow(f"{avr:.2f}"))
        print()


if __name__ == '__main__':
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
    first_guesses = {4: "LERS",
                     5: "SARTE",
                     6: "ARTENS",
                     7: "LORTENS",
                     8: "UTROLIGS"}

    # Setup the game
    game = Game(word_length=5, alphabet=alphabet, max_attempts=6)
    bot = Bot(game)

    # play games
    bot.play(1000, first_guesses=first_guesses, show=True)

    # get summary
    bot.print_stats()
