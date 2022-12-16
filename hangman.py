import sys
import re
import getpass
import random


def main():
    phrase_type = set_phrase_type()
    phrase = generate_phrase(phrase_type)
    game = Game(phrase)
    game.play_game()


# Ask user for custom or random phrase to be guessed
def set_phrase_type():
    while True:
        try:
            phrase_type = input("Custom or random phrase (c/r)?: ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit()
        if phrase_type != "c" and phrase_type != "r":
            print("Please input c or r")
        else:
            return phrase_type


# Either generate a random phrase or format a phrase the user inputs based on phrase type chosen prior
def generate_phrase(phrase_type):
    if phrase_type == "r":
        return random_phrase()
    else:
        while True:
            try:
                phrase = getpass.getpass("Input phrase: ").strip()
            except (EOFError, KeyboardInterrupt):
                sys.exit()
            if bool(re.search(r"[^a-zA-Z\.,\!?\"'& -]", phrase)):
                print(
                    "Phrase cannot contain numbers or any punctuation other than ,.?!\"&'"
                )
            elif len(phrase) == 0 or bool(re.search(r"[a-zA-z]", phrase)) == False:
                continue
            else:
                return phrase


# Select a random phrase from the list of phrases in phrases.txt
def random_phrase():
    phrases = []
    f = open("phrases.txt", "r")
    for line in f:
        phrases.append(line.strip().capitalize())
    return phrases[random.randint(0, (len(phrases) - 1))]


# Helper function to unpuncuate a phrase or guess when guessing an entire phrase
def unpunctuate(s):
    unpunctuated = ""
    for char in s:
        if bool(re.search(r"[\.,\!?\"'&-]", char)):
            continue
        unpunctuated += char
    return unpunctuated


class Game:
    # Set up empty arrays to hold correct and incorrect guesses
    correct_guesses = []
    incorrect_guesses = []

    # Initialize the game function to include the phrase the user has chosen
    def __init__(self, phrase):
        self.phrase = phrase
        self.unpunctuated_phrase = unpunctuate(phrase)

    # Display the initial hangman visual and start the game loop
    def play_game(self):
        print("Let's play hangman! You can guess a letter or the complete phrase!")
        self.update_display()
        while True:
            self.play_round()

    # Request a guess from the user and check if the guess is correct or not
    def play_round(self):
        # Keep looping through the guess prompt until a valid guess is given
        while True:
            try:
                guess = input("Guess: ").lower()
            except ValueError:
                print("Guess must be 1 letter")
                continue
            except (EOFError, KeyboardInterrupt):
                sys.exit()
            # If the user guesses the whole phrase either with all punctuation or with no punctuation the user wins
            if (
                unpunctuate(guess).lower() == self.unpunctuated_phrase.lower()
                or guess.lower() == self.phrase.lower()
            ):
                for char in set(guess):
                    self.correct_guesses.append(char)
                self.win()
            elif len(guess) != 1 or guess.isalpha() == False:
                print("Guess must be 1 letter")
            elif guess in self.incorrect_guesses or guess in self.correct_guesses:
                print("Letter has already been guessed")
            else:
                break
        # Check if the guessed letter is correct or not and add it to the appropriate array
        if guess in set(self.phrase.lower()):
            self.correct_guesses.append(guess)
            print("Correct!")
        else:
            self.incorrect_guesses.append(guess)
            print("Incorrect!")
        # Check if the user won, otherwise update the display
        self.check_win()
        self.update_display()

    # Helper function to update the display with the hangman visual and the phrase
    def update_display(self):
        self.print_visual()
        self.print_phrase()

    # Check if the user has either lost or won, if neither keep the game loop going
    def check_win(self):
        if len(self.incorrect_guesses) == 6:
            self.lose()
        for char in set(self.phrase):
            if char.isalpha() and char.lower() not in self.correct_guesses:
                return
        self.win()

    # If the user has won, end the game
    def win(self):
        self.update_display()
        print("Congratulations, you won!\n\n", end="")
        sys.exit()

    # If the user has lost, display the phrase and end the game
    def lose(self):
        self.update_display()
        print(f"The phrase was: {self.phrase}")
        print("Sorry, you lost.\n\n", end="")
        sys.exit()

    # Print the phrase, for each correctly guessed letter print the letter itself, otherwise print a placeholder "_"
    def print_phrase(self):
        for char in self.phrase:
            if char.isalpha() and char.lower() not in self.correct_guesses:
                print("_ ", end="")
            else:
                print(char + " ", end="")
        print("\n\n", end="")

    # Print a hangman visual based on how many incorrect guesses the user currently has
    def print_visual(self):
        match len(self.incorrect_guesses):
            case 0:
                print(" _______")
                print(" |   \ |")
                print("      \|")
                print("       |")
                print("       |")
                print("       |")
                print("      /|\\")
                print("     / | \\")
                print("¯¯¯¯¯¯¯¯¯¯¯")
            case 1:
                print(" _______")
                print(" |   \ |")
                print(" O    \|")
                print("       |")
                print("       |")
                print("       |")
                print("      /|\\")
                print("     / | \\")
                print("¯¯¯¯¯¯¯¯¯¯¯")
            case 2:
                print(" _______")
                print(" |   \ |")
                print(" O    \|")
                print(" |     |")
                print(" |     |")
                print("       |")
                print("      /|\\")
                print("     / | \\")
                print("¯¯¯¯¯¯¯¯¯¯¯")
            case 3:
                print(" _______")
                print(" |   \ |")
                print(" O    \|")
                print("\|     |")
                print(" |     |")
                print("       |")
                print("      /|\\")
                print("     / | \\")
                print("¯¯¯¯¯¯¯¯¯¯¯")
            case 4:
                print(" _______")
                print(" |   \ |")
                print(" O    \|")
                print("\|/    |")
                print(" |     |")
                print("       |")
                print("      /|\\")
                print("     / | \\")
                print("¯¯¯¯¯¯¯¯¯¯¯")
            case 5:
                print(" _______")
                print(" |   \ |")
                print(" O    \|")
                print("\|/    |")
                print(" |     |")
                print("/      |")
                print("      /|\\")
                print("     / | \\")
                print("¯¯¯¯¯¯¯¯¯¯¯")
            case 6:
                print(" _______")
                print(" |   \ |")
                print(" O    \|")
                print("\|/    |")
                print(" |     |")
                print("/ \    |")
                print("      /|\\")
                print("     / | \\")
                print("¯¯¯¯¯¯¯¯¯¯¯")


if __name__ == "__main__":
    main()
