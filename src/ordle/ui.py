from letter import Letter

INDENT = 14


def green(word):
    return f"\033[92m{word}\033[0m"


def yellow(word):
    return f"\033[93m{word}\033[0m"


def black(word):
    return f"\033[90m{word}\033[0m"


def blue(word):
    return f"\033[94m{word}\033[0m"


def cyan(word):
    return f"\033[96m{word}\033[0m"


def red(word):
    return f"\033[91m{word}\033[0m"


def bold(word):
    return f"\033[1m{word}\033[0m"


def clear_screen():
    print("\033[2J\033[H")


def get_input():
    print(" > ", end="")
    user_input = input().upper()
    print("\033[F\033[2K", end="")
    return user_input


def print_title(caption):
    print()
    with open("src/ordle/title.txt") as f:
        print(f.read())
    print(f"- {caption}")
    print()


def print_instructions(text):
    print(cyan(text))
    print()


def colorize(let):
    if let.state == Letter.State.CORRECT:
        return green(let.value)
    elif let.state == Letter.State.INCLUDED:
        return yellow(let.value)
    elif let.state == Letter.State.EXCLUDED:
        return black(let.value)
    else:
        return let.value


def print_letters(game, backtrack=0, end="\n"):
    if backtrack > 0:
        print(f"\033[{backtrack}F", end="")
    for c in game.alphabet:
        print(bold(colorize(game.letters[c])), end="")
    print("", end=end)
    if backtrack > 0:
        print(f"\033[{backtrack}E", end="")


def print_guess(game, number=-1):
    if number == -1:
        print(cyan(f"{game.attempts_used()}: "), end="")
    else:
        print(cyan(f"{number + 1}: "), end="")

    for let in game.guesses[number]:
        print(bold(colorize(let)), end="")


def calc_line_width(word_length, attempts):
    return INDENT + (word_length + 5) * attempts + 1


def print_game_word(word, attempts):
    word_length = len(word)
    print(bold(black(f"{word}")), end=" ")
    print_line(calc_line_width(word_length, attempts) - word_length - 1)


def print_word_line(word, game):
    print(bold(cyan(f"{word}")), end=" ")
    print_line(
        calc_line_width(game.word_length, game.max_attempts) - len(word) - 1,
        color=cyan,
    )


def print_inline_game(game, player):
    if len(player) > INDENT:
        player = f"{player[0: INDENT - 3]}..."
    player = player.rjust(INDENT)
    name = red(player) if not game.get_state() == game.State.WIN else green(player)
    print(black(name), end=black(" | "))
    for i in range(game.attempts_used()):
        print_guess(game, number=i)
        print("  ", end="")
    print()


def print_line(length, color=black):
    print(color(bold("\u2015" * length)))


def print_summary(game):
    print()
    if game.get_state() == game.State.WIN:
        print(green("YOU WON! "), end="")
        print(f"{game.attempts_used()} attemps used")
    else:
        print(red("YOU LOST! "), end="")
        print(f"The word was: {game.get_answer()}")
    print()


def print_stats(names, win_rates, averages, n, game):
    print()
    print()
    print_word_line(f"SUMMARY ({n} games played)", game)
    print()
    print("Bot Name".rjust(INDENT), end=black(" | "))
    print("Success Rate".ljust(12), end=black(" | "))
    print("Average Attempts")

    for i in range(len(names)):
        print(yellow(names[i].rjust(INDENT)), end=black(" | "))
        print(yellow(f"{win_rates[i]:.1f}%".ljust(12)), end=black(" | "))
        if averages[i] is not None:
            print(yellow(f"{averages[i]:.2f}"))
        else:
            print(yellow("-"))
    print()
