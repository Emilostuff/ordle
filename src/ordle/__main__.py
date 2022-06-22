import argparse
import ui
from game import Game
from tester import BotTester

# Bots
from bots.emilobot import EmiloBot

# Game settings
CAPTION = "The Danish version of Wordle"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
LENGTH = 5
ATTEMPTS = 6

# Testing
ALL_BOTS = [EmiloBot]
BOT_UNDER_DEV = None


def play(game):
    # Print Title
    ui.clear_screen()
    ui.print_title(caption=CAPTION)
    ui.print_instructions(
        f"Guess the {LENGTH} letter word. You have {ATTEMPTS} attempts!"
    )

    # Print letter status first time
    ui.print_letters(game, end="\n")
    ui.print_line(len(ALPHABET))

    # Play the game
    lines = 1
    while game.get_state() == Game.State.ACTIVE:
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


if __name__ == "__main__":
    # setup game
    game = Game(word_length=LENGTH, alphabet=ALPHABET, max_attempts=ATTEMPTS)

    # setup args
    ps = argparse.ArgumentParser(description=CAPTION)
    ps.add_argument("-t", help="Run in test mode", action="store_const", const=True)
    ps.add_argument(
        "-dev", help="Test only bot under development", action="store_const", const=True
    )
    ps.add_argument("-n", type=int, help="Number of games to be played in test mode")
    ps.add_argument(
        "-show", help="Show games in test mode", action="store_const", const=True
    )
    ps.add_argument("-seed", type=int, help="Use specific seed in test mode")

    # parse args
    args = ps.parse_args()
    n = args.n if args.n is not None else 100
    show = True if args.t is not None else False

    if args.t:
        # introduce test mode
        ui.print_title(caption=CAPTION)
        ui.print_word_line("TESTING BOTS", game)
        print()

        # collect bots staged for testing
        bots_to_test = []
        if not args.dev:
            bots_to_test.extend(ALL_BOTS)
        if BOT_UNDER_DEV and BOT_UNDER_DEV not in bots_to_test:
            bots_to_test.append(BOT_UNDER_DEV)
        if len(bots_to_test) < 1:
            raise RuntimeError("No bots staged for testing!")

        # run tests
        tester = BotTester(game, bots_to_test)
        tester.run(n=n, show=show, seed=args.seed)
    else:
        play(game)
