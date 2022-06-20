from bot import Bot
from game import Game
import bot_utils


class MyBot(Bot):

    def play(self):
        candidates = self.game.wordlist
        info = bot_utils.Info(game)

        # first guess
        if not hasattr(self, "first_guess"):
            self.first_guess = bot_utils.pick_best(candidates, info)
        guess = self.first_guess

        # Game loop
        for _ in range(self.game.max_attempts):
            # make guess and check win
            self.game.make_guess(guess)
            info.guesses.append(guess)

            # check for game over
            if self.game.state != Game.State.ACTIVE:
                return

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


if __name__ == '__main__':
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
    word_length = 5

    # Setup the game
    game = Game(word_length=word_length, alphabet=alphabet, max_attempts=6)
    bot = MyBot(game)

    # play games
    bot.test(100, show=True, seed=1)

    # get summary
    bot.print_stats()
