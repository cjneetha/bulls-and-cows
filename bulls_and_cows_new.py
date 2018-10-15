import sys
import os
import pickle
import random

# dictionary file name
FOUR_LETTER_WORDS_DICTIONARY = "4lwords.p"

# words dictionary
all_words = []

# saved user words
SAVED_USER_WORDS_FILE = "/Users/jtadipatri/4luserwords.p"
all_user_guesses = []

def load_saved_user_words():
    global all_user_guesses
    global SAVED_USER_WORDS_FILE

    # nothing to do if file doesn't exists..
    # happens on first run
    if not os.path.isfile(SAVED_USER_WORDS_FILE):
        return

    with open(SAVED_USER_WORDS_FILE, 'rb') as fh:
        all_user_guesses = pickle.load(fh)
    return

def dump_saved_user_words(more_words):
    global all_user_guesses
    global SAVED_USER_WORDS_FILE

    # merge 2 lists before writing back to file
    all_user_guesses = list(set(all_user_guesses + more_words))

    with open(SAVED_USER_WORDS_FILE, 'wb') as fh:
        pickle.dump(all_user_guesses, fh, protocol = pickle.HIGHEST_PROTOCOL)
    return

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

def user_guesses():
    global all_words
    random_word = random.choice(all_words)
    print("Okay!..I'm ready..\nIf you would like to quit this game, enter " + \
          "\"_quit\" instead of word you guess")
    ntries = 0
    guessed_words = {}
    while True:
        user_guess = input("Guess the word: ").strip().upper()
        if user_guess == "_QUIT":
            print("Gave up after %r attempts. Word was %s" % (ntries, random_word))
            break

        if user_guess not in all_words:
            print("Word %s not found in dictionary. Guess again..." % \
                (user_guess))
            continue

        if user_guess in guessed_words:
            print("You already guessed %s on attempt #%r" % (user_guess, \
                guessed_words[user_guess]))
            continue

        ntries += 1
        guessed_words[user_guess] = ntries
        (bulls, cows) = calculate_bulls_and_cows(random_word, user_guess)

        # if 4 bulls = found word
        if bulls == 4:
            print("Guessed the right word %r in %r attempts." % \
                (random_word, ntries))
            break
        else:
            print("Your word %s has %r bulls and %r cows. Guess again..." % \
                (user_guess, bulls, cows))

    # save all user guessed words for machine guesses..
    dump_saved_user_words(guessed_words.keys())
    return

def machine_guesses():
    global all_words
    global all_user_guesses

    # load words user has guessed so far
    ### No need to do this here...can be improved..
    load_saved_user_words()

    ## make a copy for machine guess list
    curr_user_guesses = all_user_guesses[:]
    curr_all_words = all_words[:]

    print("Loaded and ready with %d user words and %d dictionary words" % \
        (len(curr_user_guesses), len(curr_all_words)))
    print("Think of a word and hit enter to continue...")
    input()

    ntries = 0
    while True:
        ## for now, guess a word from curr_user_guesses and if nothing available
        ## on that list, go to curr_all_words
        my_guess = None
        if curr_user_guesses:
            my_guess = random.choice(curr_user_guesses)
        elif curr_all_words:
            my_guess = random.choice(curr_all_words)
        else:
            print("Ran out of all words!!...I give up..")
            break

        assert my_guess, "Cannot say empty word to user..."

        my_guess = my_guess.strip().upper()
        ntries += 1

        # get user feedback about word
        (bulls, cows) = (None, None)
        while True:
            print("Is \"%s\" the word you've thought of?" % (my_guess))
            bc = input("Please enter csv'ed number of bulls & cows: ").strip()
            sbc = [x.strip() for x in bc.split(",")]
            if len(sbc) != 2 and not (sbc[0].isdigit() and sbc[1].isdigit()):
                print("Please enter bulls and cows separated by comma")
                continue
            (bulls, cows) = (int(sbc[0]), int(sbc[1]))
            break

        if bulls == 4: # done
            print("Great!!..Took %r tries to guess the word" % (ntries))
            break

        # filter words by user feedback
        if cows + bulls == 0:
            # none of the letters in guessed word are in user's word
            def remove_words_from_list(myw, ltp):
                ret_list = []
                for w in ltp:
                    include_word = True
                    for c in myw:
                        if c in w:
                            include_word = False
                            continue
                    if include_word: ret_list.append(w)
                return ret_list

            curr_all_words = remove_words_from_list(my_guess, curr_all_words)
            curr_user_guesses = remove_words_from_list(my_guess, curr_user_guesses)

        if bulls > 0 or cows > 0:
            # match exact number of bulls in lists
            def match_bulls(myw, ltp, bulls, cows):
                ret_list = []
                for w in ltp:
                    (b, c) = calculate_bulls_and_cows(myw, w)
                    if bulls > 0 and b == bulls: ret_list.append(w)
                    elif cows > 0 and c >= cows: ret_list.append(w)
                return ret_list

            curr_all_words = match_bulls(my_guess, curr_all_words, bulls, cows)
            curr_user_guesses = match_bulls(my_guess, curr_user_guesses, bulls, cows)
        pass # top level while loop
    return

def start_game():
    begin_text="""Game has 2 modes for now. Either you can think of a valid
    word and make the system guess it. Or you can let the machine think of
    a word and you can guess it. Please choose an option from below to proceed..
    """
    print(begin_text)
    gs = "0. Exit\n1. Machine guesses your word.\n2. You guess machine's word\n"
    while True:
        game_mode = input(gs + "Enter your choice: ").strip()
        if game_mode == "1":
            machine_guesses()
            break
        elif game_mode == "2":
            user_guesses()
            break
        elif game_mode == "0":
            break
        else:
            print("Invalid selection...")
    return

if __name__ == '__main__':
    # exit if failed to load dictionary
    if not load_dictionary(FOUR_LETTER_WORDS_DICTIONARY):
        sys.exit(1)

    #print("Words loaded from pickle ", len(all_words))
    show_game_rules()
    start_game()

