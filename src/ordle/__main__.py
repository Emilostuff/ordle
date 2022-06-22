import ui
import sys
from game import Game
from tester import BotTester
from bots.emilobot import EmiloBot

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
LENGTH = 5
ATTEMPTS = 6
BOTS = [EmiloBot]


def play(game):
    # Print Title
    ui.clear_screen()
    ui.print_title(caption="The Danish version of Wordle")
    ui.print_instructions(
        f"Guess the {LENGTH} letter word. You have {ATTEMPTS} attempts!"
    )

    # Print letter status first time
    ui.print_letters(game, end="\n")
    ui.print_line(len(ALPHABET))

    # Play the game
    lines = 1
    while game.state == Game.State.ACTIVE:
        # Take a guess
        while True:
            user_input = ui.get_input()
            if game.make_guess(user_input):
                break

        # Print result
        ui.print_guess(game)
        lines += 1

        # move back and reprint letter status
        ui.print_letters(game, backtrack=lines, end="\n")

    # Game summary
    ui.print_line(len(ALPHABET))
    ui.print_summary(game)


def test(game):
    ui.print_title(caption="The Danish version of Wordle")
    ui.print_word_line("BOT PERFORMANCE TESTS", game)
    print()
    # run tests
    tester = BotTester(game, BOTS)
    tester.run(n=int(sys.argv[2]), show=True, seed=0)


def show_help(game):
    ui.print_title(caption="The Danish version of Wordle")
    ui.print_word_line("USAGE", game)
    print("PLAY: python3 src/ordle")
    print("TEST: python3 src/ordle test [number of games]")


if __name__ == "__main__":
    game = Game(word_length=LENGTH, alphabet=ALPHABET, max_attempts=ATTEMPTS)

    if len(sys.argv) == 1:
        play(game)
    elif len(sys.argv) == 3 and sys.argv[1] == "test" and sys.argv[2].isnumeric():
        test(game)
    else:
        show_help(game)
