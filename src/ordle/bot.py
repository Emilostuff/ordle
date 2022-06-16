from game import Game
from letter import Letter


class Result:
    def __init__(self, win, attempts):
        self.win = win
        self.attempts = attempts


class Bot:
    def __init__(self, game):
        self.game = game
        self.results = []
        self.word_length = len(self.game.wordlist)
        self.reset()

    def reset(self):
        self.candidates = self.game.wordlist
        self.included = set()
        self.excluded = set()
        self.correct = [None] * self.word_length
        self.incorrect = [set() for _ in range(self.word_length)]
        self.guesses = []
        self.game.restart()

    def pick(self):
        # tally up character occurences
        chars = [dict()] * (self.word_length)
        for word in self.candidates:
            for (i, c) in enumerate(word):
                if c in chars[i]:
                    chars[i][c] += 1
                else:
                    chars[i][c] = 1

        # score each word
        best_score = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        best_words = dict()

        for word in self.candidates:
            score = 0
            letters = set()
            for (i, c) in enumerate(word):
                score += chars[i][c]
                letters.add(c)
            if score > best_score[len(letters)] and word not in self.guesses:
                best_score[len(letters)] = score
                best_words[len(letters)] = word

        for i in range(5, 1, -1):
            if i in best_words.keys():
                return best_words[i]

    def parse(self):
        res = self.game.last_guess()
        for (i, let) in enumerate(res):
            if let.state == Letter.State.INCLUDED:
                self.included.add(let.value)
                self.incorrect[i].add(let.value)
            elif let.state == Letter.State.EXCLUDED:
                self.excluded.add(let.value)
            elif let.state == Letter.State.CORRECT:
                self.correct[i] = let.value

    def filter(self):
        to_keep = []
        for word in self.candidates:
            def check():
                for (i, c) in enumerate(word):
                    if self.correct[i] is not None and self.correct[i] != c:
                        return
                    elif c in self.incorrect[i]:
                        return
                    elif c in self.excluded:
                        return
                for c in self.included:
                    if c not in word:
                        return
                to_keep.append(word)

            check()

        self.candidates = to_keep

    def play(self, n):
        for _ in range(n):
            self.reset()
            guess = "RESAT"
            # Game loop
            for _ in range(self.game.max_attempts):
                # make guess and check win
                print(f"Chose: {guess} from {len(self.candidates)}")
                game.make_guess(guess)
                self.guesses.append(guess)
                if game.state != Game.State.ACTIVE:
                    win = game.state == Game.State.WIN
                    attempts = self.game.attempts_used()
                    self.results.append(Result(win, attempts))
                    print(win, attempts)
                    break

                # parse result and filter wordlist
                self.parse()
                self.filter()

                # pick a new guess
                guess = self.pick()

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

        print(f"Won {rate:.1f}% of games. Used on average {avr:.2f} attempts")


if __name__ == '__main__':
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
    # Setup the game
    game = Game(word_length=5, alphabet=ALPHABET, max_attempts=10)

    # play games
    bot = Bot(game)
    bot.play(1000)
    bot.print_stats()
