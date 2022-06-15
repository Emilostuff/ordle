from game import Game
import ui

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
LENGTH = 5
ATTEMPTS = 6

if __name__ == '__main__':
    # Setup the game
    game = Game(word_length=LENGTH, alphabet=ALPHABET, max_attempts=ATTEMPTS)

    # Print Title
    ui.clear_screen()
    ui.print_title(caption="The Danish version of Wordle")
    ui.print_instructions(
        f"Guess the {LENGTH} letter word. You have {ATTEMPTS} attempts!")

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
