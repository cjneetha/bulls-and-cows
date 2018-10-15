# bulls-and-cows

"""Goal of the game is to guess the 4-letter word the sytem has
    thought of in least number of tries. All words have unique characters.

        - A bull is when a character of your guessed word is in exact position in
          target word.
        - A cow is when a character of your guessed word is in a different position
          in target word.
    For example, if your guess word is COWS and target word is WORD, it will have
        - 1 bull, since O in COWS (index 2) is in exact position of that in WORD (index 2)
        - 1 cow,  since W in COWS (index 3) is in different position of that in WORD (index 1)
    """
