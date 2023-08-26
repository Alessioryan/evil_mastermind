# Creates a Mastermind board object
from collections import defaultdict


class Mastermind:
    # Create a mastermind object with a given number of holes
    def __init__(self, num_colors, num_holes):
        # Define the given values
        self.num_colors = num_colors
        self.num_holes = num_holes

        # Create all the possibilities
        temp_possibilities = [[color] for color in range(self.num_colors)]
        for i in range(self.num_holes - 1):
            building_possibilities = []
            for temp_possibility in temp_possibilities:
                for color in range(self.num_colors):
                    appended_color = list(temp_possibility)
                    appended_color.append(color)
                    building_possibilities.append(appended_color)
            temp_possibilities = building_possibilities
        self.possibilities = set([tuple(possibility) for possibility in temp_possibilities])

        # Create an object for past guesses
        self.past_guesses = []

    # Runs a round, asking the player to guess a combination and printing the feedback
    def run_round(self):
        # Print the previous rounds, if applicable
        if len(self.past_guesses):
            self.print_previous_rounds()

        # Get the user's guess
        guess = self.get_guess()
        print(f"You guessed {guess}")

        # Find the outcome for the possibilities given the guess
        results = defaultdict(set)
        for possibility in self.possibilities:
            result = self.find_result(guess, possibility)
            results[result].add(possibility)

        # Choose the result with the most possibilities
        max_key = max(results, key=lambda key: len(results[key]))

        # Save the guess and set the new possibilities to those with the max key
        self.past_guesses.append((guess, max_key))
        self.possibilities = results[max_key]

        # Print a new line to keep it clean
        print()

    # Finds the result given a guess and a possibility
    def find_result(self, guess, possibility):
        # Find the number of black ones
        blacks = 0
        for i in range(self.num_holes):
            if guess[i] == possibility[i]:
                blacks += 1

        # Find the number of white ones
        whites = 0
        for color in range(self.num_colors):
            whites += min(guess.count(color), possibility.count(color) )
        whites -= blacks

        # Return a tuple of (blacks, whites)
        return blacks, whites

    # Gets the user's guess
    def get_guess(self):
        # Ask for the guess
        preprocessed_guess = ""
        while not preprocessed_guess:
            preprocessed_guess = input("What would you like to guess? ").strip()
            if not preprocessed_guess:  # Debug method for showing possibilities
                self.print_possibilities()
                print('Possibilities revealed.')
            else:  # Check to see that it fits our requirements
                if len(preprocessed_guess) != self.num_holes:  # It must have the right length
                    print(f'Please provide a guess with {self.num_holes} numbers.')
                else:
                    try:
                        if "." in preprocessed_guess or "-" in preprocessed_guess:
                            raise ValueError()  # It must not be a decimal or a negative
                        number_tuple = tuple([int(character) for character in str(preprocessed_guess)])
                        for number in number_tuple:
                            if number >= self.num_colors:
                                raise ValueError()  # It must only contain digits equal to the number of colors
                        return number_tuple
                    except ValueError:
                        print(f'Please only provide digits from 0 to {self.num_colors - 1}')
            preprocessed_guess = ""
            print()

    # Prints the previous guesses and their outcomes
    def print_previous_rounds(self):
        for index, (previous_guess, result) in enumerate(self.past_guesses):
            print(f"Round {index + 1}: {previous_guess}      {result}")

    # Debug method, prints out all the possibilities for this board
    def print_possibilities(self):
        print(f'There are {len(self.possibilities)} possibilities.')
        print(self.possibilities)


# Runs a game given parameters
def run_game(num_colors=8, num_holes=5):
    # Create a mastermind object
    board = Mastermind(num_colors, num_holes)
    print('Game is starting.')

    # Run until the game is over
    while len(board.possibilities) != 1:
        board.run_round()

    # Finish the game
    print(f'You won in {len(board.past_guesses)}!')


# Gets the info for a game
def start_game():
    # Get all the info about the goals for the game
    # TODO Account for people who don't put numbers here
    num_colors = int(input("How many colors do you want to play with? ") )
    if num_colors > 10:
        print('--> Only 10 colors are handled at the moment. Setting the number of colors to 10...')
        num_colors = 10
    num_holes = int(input("How many holes do you want to play with? ") )

    # Run a game with the parameters
    run_game(num_colors, num_holes)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_game()

