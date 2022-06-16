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

    def play(self, n, first_guess, show=True):
        # check first guess
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
                self.game.make_guess(guess)
                info.guesses.append(guess)

                # print guess
                if show:
                    print_guess(self.game)
                    print("  ", end="")

                # check for game over
                if self.game.state != Game.State.ACTIVE:
                    win = self.game.state == Game.State.WIN
                    attempts = self.game.attempts_used()
                    self.results.append(Result(win, attempts))
                    if show:
                        print(red("[DEFEAT]") if not win else "")
                    break

                # parse result and filter wordlist
                bot_utils.parse_guess(self.game, info)
                candidates = bot_utils.filter(candidates, info)

                # pick a new guess
                
                if info.no_included and self.game.attempts_left() > 1:
                    # guess entirely new letters
                    temp_info = bot_utils.Info(self.game)
                    available = bot_utils.get_available_chars(candidates)
                    available.difference_update(info.included)
                    available.difference_update(set(info.correct))

                    for c in self.game.alphabet:
                        if c not in available:
                            temp_info.excluded.add(c)

                    words = bot_utils.filter(self.game.wordlist, temp_info)
                    guess = bot_utils.pick_best(words, temp_info)
                    if guess is not None:
                        continue

                # otherwise make normal guess
                guess = bot_utils.pick_best(candidates, info)

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


if __name__ == '__main__':
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
    word_length = 5
    first_guesses = {4: "LERS",
                     5: "RASET",
                     6: "ARTENS",
                     7: "LORTENS",
                     8: "UTROLIGS"}

    # Setup the game
    game = Game(word_length=word_length, alphabet=alphabet, max_attempts=6)
    bot = Bot(game)

    # play games
    bot.play(100, first_guess=first_guesses[word_length], show=True)

    # get summary
    bot.print_stats()
