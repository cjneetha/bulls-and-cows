import sys
import os
import pickle
import random

# dictionary file name
FOUR_LETTER_WORDS_DICTIONARY = "4lwords.p"

# words dictionary
all_words = []

def load_dictionary(file_name):
    global all_words
    if not os.path.isfile(file_name):
        print("Cannot find file", file_name)
        return False

    with open(file_name, 'rb') as fh:
        all_words = pickle.load(fh)

    return True

def show_game_rules():
    rules = """Goal of the game is to guess the 4-letter word the sytem has
    thought of in least number of tries. All words have unique characters.

        - A bull is when a character of your guessed word is in exact position in
          target word.
        - A cow is when a character of your guessed word is in a different position
          in target word.
    For example, if your guess word is COWS and target word is WORD, it will have
        - 1 bull, since O in COWS (index 2) is in exact position of that in WORD (index 2)
        - 1 cow,  since W in COWS (index 3) is in different position of that in WORD (index 1)
    """
    print(rules)
    return

def calculate_bulls_and_cows(base, guess):
    bulls = cows = 0
    for i in range(len(base)):
        if base[i] == guess[i]:
            bulls += 1
        elif guess[i] in base:
            cows += 1

    # some sanity checks
    assert bulls + cows <= 4, "Bug in calculating bulls and cows"
    if bulls == 4:
        assert base == guess, "Bug in comparing %s and %s" % (base, guess) 
    return (bulls, cows)

def start_game():
    global all_words
    random_word = random.choice(all_words)
    ntries = 0
    while True:
        user_guess = input("Guess the word: ").strip().upper()
        if user_guess not in all_words:
            print("Word %s not found in dictionary. Guess again..." % \
                (user_guess))
            continue
        ntries += 1
        (bulls, cows) = calculate_bulls_and_cows(random_word, user_guess)

        # if 4 bulls = found word
        if bulls == 4:
            print("Guessed the right word %r in %r attempts." % \
                (random_word, ntries))
            break
        else:
            print("Your word %s has %r bulls and %r cows. Guess again..." % \
                (user_guess, bulls, cows))
    return

if __name__ == '__main__':
    # exit if failed to load dictionary
    if not load_dictionary(FOUR_LETTER_WORDS_DICTIONARY):
        sys.exit(1)

    #print("Words loaded from pickle ", len(all_words))
    show_game_rules()
    start_game()

