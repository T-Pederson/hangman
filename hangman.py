import sys
import re


def main():
    number_of_players = set_players()
    phrase = generate_phrase(number_of_players)
    game = Game(number_of_players, phrase)
    game.play_game()


def set_players():
    number_of_players = 0
    while True:
        try:
            number_of_players = int(input("Number of players (1 or 2): "))
        except ValueError:
            print("Please input 1 or 2")
            continue
        except (EOFError, KeyboardInterrupt):
            sys.exit()
        if number_of_players != 1 and number_of_players != 2:
            print("Please input 1 or 2")
        else:
            return number_of_players


def generate_phrase(number_of_players):
    if number_of_players == 1:
        return "This is hangman"
    else:
        while True:
            try:
                phrase = input("Input word or phrase: ")
            except (EOFError, KeyboardInterrupt):
                sys.exit()
            if bool(re.search(r"[^a-zA-Z\.,\!? ]", phrase)):
                print("Word/phrase cannot contain numbers or any punctuation other than ,.?!")
            elif len(phrase) == 0 or bool(re.search(r"[a-zA-z]", phrase)) == False:
                continue
            else:
                return phrase.strip()


class Game:
    correct_guesses = []
    incorrect_guesses = []
    
    def __init__(self, number_of_players, phrase):
        self.number_of_players = number_of_players
        self.phrase = phrase

    def play_game(self):
        Game.update_display(self)
        while True:
            Game.play_round(self)

    def play_round(self):
        while True:
            try:
                guess = input("Guess: ").lower()
            except ValueError:
                print("Guess must be 1 letter")
                continue
            except (EOFError, KeyboardInterrupt):
                sys.exit()
            if len(guess) != 1 or guess.isalpha() == False:
                print("Guess must be 1 letter")
            elif guess in self.incorrect_guesses or guess in self.correct_guesses:
                print("Letter has already been guessed")
            else:
                break
        if guess in set(self.phrase.lower()):
            self.correct_guesses.append(guess)
        else:
            self.incorrect_guesses.append(guess)
        Game.check_win(self)
        Game.update_display(self)

    def update_display(self):
        Game.print_visual(self)
        Game.print_phrase(self)
    
    def check_win(self):
        if len(self.incorrect_guesses) == 6:
            Game.lose(self)
        for char in set(self.phrase):
            if char.isalpha() and char.lower() not in self.correct_guesses:
                return
        Game.win(self)
    
    def win(self):
        Game.update_display(self)
        print("Congratulations, you won!\n\n", end="")
        sys.exit()

    def lose(self):
        Game.update_display(self)
        print(f"The word/phrase was: {self.phrase}")
        print("Sorry, you lost.\n\n", end="")
        sys.exit()

    def print_phrase(self):
        for char in self.phrase:
            if char.isalpha() and char.lower() not in self.correct_guesses:
                print("_", end="")
            else:
                print(char, end="")
        print("\n\n", end="")

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
