from game import Game
import ui

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"


if __name__ == '__main__':
    # setup game
    length = 5
    attempts = 6
    game = Game(word_length=length, alphabet=LETTERS, max_attempts=attempts)
    ui.print_title(caption="The Danish version of Wordle")
    ui.print_instructions(
        f"Guess the {length} letter word. You have {attempts} attempts!")

    # Print letter status
    ui.print_letters(game, end="\n")
    ui.print_line(len(LETTERS))

    # play the game
    lines = 2
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

    # game summary
    ui.print_line(len(LETTERS))
    ui.print_summary(game)
