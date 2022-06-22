from bot import Bot
from game import Game
from letter import Letter


class Info:
    def __init__(self, game):
        self.word_length = game.word_length
        self.included = set()
        self.excluded = set()
        self.correct = [None] * self.word_length
        self.incorrect = [set() for _ in range(self.word_length)]
        self.guesses = []
        self.no_yellow = False


def update_info(game, info):
    info.no_yellow = True
    for (i, let) in enumerate(game.last_guess()):
        if let.state == Letter.State.INCLUDED:
            info.no_yellow = False
            info.included.add(let.value)
            info.incorrect[i].add(let.value)
        elif let.state == Letter.State.EXCLUDED:
            info.excluded.add(let.value)
        elif let.state == Letter.State.CORRECT:
            info.correct[i] = let.value


def filter_valid(candidates, info):
    to_keep = []
    for word in candidates:

        def check():
            for (i, c) in enumerate(word):
                if info.correct[i] is not None and info.correct[i] != c:
                    return
                elif c in info.incorrect[i] or c in info.excluded:
                    return
            for c in info.included:
                if c not in word:
                    return
            to_keep.append(word)

        check()

    return to_keep


def tally(words, info):
    chars = [dict()] * info.word_length
    for word in words:
        for (i, c) in enumerate(word):
            if c in chars[i]:
                chars[i][c] += 1
            else:
                chars[i][c] = 1
    return chars


def pick_best(candidates, info):
    # tally up character occurences
    chars = tally(candidates, info)

    # score each word
    best_score = dict()
    for i in range(1, info.word_length + 1):
        best_score[i] = 0
    best_words = dict()

    for word in candidates:
        score = 0
        matching_letters = set()
        for (i, c) in enumerate(word):
            if c not in info.excluded:
                score += chars[i][c]
                matching_letters.add(c)
        if len(matching_letters) < 1:
            continue
        if score > best_score[len(matching_letters)] and word not in info.guesses:
            best_score[len(matching_letters)] = score
            best_words[len(matching_letters)] = word

    for i in range(info.word_length, 1, -1):
        if i in best_words.keys():
            return best_words[i]


def get_available_chars(candidates):
    available = set()
    for word in candidates:
        for c in word:
            available.add(c)
    return available


class EmiloBot(Bot):
    def play(self, game):
        # setup
        candidates = game.wordlist
        info = Info(game)

        # save first guess (since it will not change)
        if not hasattr(self, "first_guess"):
            self.first_guess = pick_best(candidates, info)
        guess = self.first_guess

        # Game loop
        for _ in range(game.max_attempts):
            # make guess
            game.make_guess(guess)

            # check for game over
            if game.get_state() != Game.State.ACTIVE:
                return

            # parse result and filter wordlist
            info.guesses.append(guess)
            update_info(game, info)
            candidates = filter_valid(candidates, info)

            # pick a new guess
            if info.no_yellow and game.attempts_left() > 1:
                # guess entirely new letters
                temp_info = Info(game)
                available = get_available_chars(candidates)
                available.difference_update(info.included)
                available.difference_update(set(info.correct))

                for c in game.alphabet:
                    if c not in available:
                        temp_info.excluded.add(c)

                guess = pick_best(game.wordlist, temp_info)
                if guess is not None:
                    continue

            # otherwise make normal guess
            guess = pick_best(candidates, info)
