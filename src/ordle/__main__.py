import random

MAX_TRIES = 6
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"


def get_input(valid):
    while True:
        print(" > ", end="")
        user_input = input().upper()
        print("\033[F\033[2K\033[1G", end="")
        if user_input in valid:
            return user_input


def green(word):
    return f"\033[92m{word}\033[0m"


def yellow(word):
    return f"\033[93m{word}\033[0m"


def black(word):
    return f"\033[90m{word}\033[0m"


def cyan(word):
    return f"\033[96m{word}\033[0m"


def bold(word):
    return f"\033[1m{word}\033[0m"


if __name__ == '__main__':
    # load words
    f = open('words.txt')
    words = f.read().splitlines()

    # choose secret word
    word = random.choice(words)

    # status
    attempts = 0
    alphabet = [c for c in LETTERS]
    win = False

    # play the game
    print("WELCOME TO ORDLE - THE DANISH VERSION OF WORDLE")
    while attempts < MAX_TRIES:
        attempts += 1
        guess = get_input(words)

        # print word with colors
        print(cyan(f"{attempts}: "), end="")
        for (i, c) in enumerate(guess):
            out = black(c)
            if c == word[i]:
                out = green(c)
            elif c in word:
                out = yellow(c)
            print(bold(out), end="")
            alphabet[LETTERS.index(c)] = out

        # print status
        print(cyan("   STATUS: "), end="")
        print("".join(alphabet))

        # Check win
        if guess == word:
            win = True
            break

    # summary
    if win:
        print(f"YOU WON!\n{attempts} attemps used.")
    else:
        print(f"YOU LOST!\nThe correct word was: {word}")
