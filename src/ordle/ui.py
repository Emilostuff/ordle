from letter import Letter


def green(word):
    return f"\033[92m{word}\033[0m"


def yellow(word):
    return f"\033[93m{word}\033[0m"


def black(word):
    return f"\033[90m{word}\033[0m"


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


def print_letters(game, backtrack=0, end='\n', ):
    if backtrack > 0:
        print(f"\033[{backtrack}F", end="")
    for c in game.alphabet:
        print(bold(colorize(game.letters[c])), end="")
    print("", end=end)
    if backtrack > 0:
        print(f"\033[{backtrack}E", end="")


def print_guess(game):
    print(cyan(f"{game.attempts_used()}: "), end="")

    for let in game.last_guess():
        print(bold(colorize(let)), end="")


def print_line(length):
    print(black(bold("\u2015" * length)))


def print_summary(game):
    print()
    if game.state == game.State.WIN:
        print(green("YOU WON! "), end="")
        print(f"{game.attempts_used()} attemps used")
    else:
        print(red("YOU LOST! "), end="")
        print(f"The word was: {game.get_answer()}")
    print()
