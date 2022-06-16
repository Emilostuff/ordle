from letter import Letter


class Info:
    def __init__(self, game):
        self.word_length = game.word_length
        self.included = set()
        self.excluded = set()
        self.correct = [None] * self.word_length
        self.incorrect = [set() for _ in range(self.word_length)]
        self.guesses = []


def parse(game, info):
    for (i, let) in enumerate(game.last_guess()):
        if let.state == Letter.State.INCLUDED:
            info.included.add(let.value)
            info.incorrect[i].add(let.value)
        elif let.state == Letter.State.EXCLUDED:
            info.excluded.add(let.value)
        elif let.state == Letter.State.CORRECT:
            info.correct[i] = let.value


def filter(candidates, info):
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


def pick(candidates, info):
    # tally up character occurences
    chars = [dict()] * info.word_length
    for word in candidates:
        for (i, c) in enumerate(word):
            if c in chars[i]:
                chars[i][c] += 1
            else:
                chars[i][c] = 1

    # score each word
    best_score = dict()
    for i in range(1, info.word_length + 1):
        best_score[i] = 0
    best_words = dict()

    for word in candidates:
        score = 0
        letters = set()
        for (i, c) in enumerate(word):
            score += chars[i][c]
            letters.add(c)
        if score > best_score[len(letters)] and word not in info.guesses:
            best_score[len(letters)] = score
            best_words[len(letters)] = word

    for i in range(info.word_length, 1, -1):
        if i in best_words.keys():
            return best_words[i]
