# SC1001 Week 9 - Functions
# 1A2B (Bulls & Cows) game

import random


def generate_target():
    """Randomly pick 4 DIFFERENT digits and return them as a string, e.g. '2468'.
    Parameters: none
    Returns: str of length 4
    """
    digits = random.sample("0123456789", 4)   # 4 distinct digits, as a list
    return "".join(digits)                    # ['2','4','6','8'] -> '2468'


def is_valid_guess(guess):
    """Check that the guess is exactly 4 different digits.
    Parameters: guess (str)
    Returns: bool
    """
    if len(guess) != 4:
        return False
    if not guess.isdigit():
        return False
    if len(set(guess)) != 4:                  # a set removes duplicates
        return False
    return True


def get_guess():
    """Keep asking the player until they type a valid guess.
    Parameters: none
    Returns: str of length 4
    """
    guess = input("Please input 4 digits: ")
    while not is_valid_guess(guess):
        print("Invalid! Enter 4 different digits, e.g. 1234.")
        guess = input("Please input 4 digits: ")
    return guess


def count_bulls_cows(target, guess):
    """Compare the guess with the target.
    Parameters: target (str), guess (str)
    Returns: tuple (bulls, cows)
    """
    bulls = 0
    cows = 0
    for i in range(4):
        if guess[i] == target[i]:             # right digit, right position
            bulls += 1
        elif guess[i] in target:              # right digit, wrong position
            cows += 1
    return bulls, cows


def show_result(bulls, cows):
    """Print the result of one round.
    Parameters: bulls (int), cows (int)
    Returns: None
    """
    print(bulls, "A (Bulls)", cows, "B (Cows)")


def play_game():
    """Run the whole game: pick a target, loop over rounds until 4A.
    Parameters: none
    Returns: int, the number of attempts taken
    """
    target = generate_target()
    attempts = 0
    bulls = 0
    while bulls != 4:
        guess = get_guess()
        attempts += 1
        bulls, cows = count_bulls_cows(target, guess)
        if bulls != 4:
            show_result(bulls, cows)
    print("You Win!!")
    print("Attempts:", attempts)
    return attempts


play_game()
