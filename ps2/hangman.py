# 2023-07-16
# Problem Set 2, hangman.py
# Name: Huzaifa Syed
# Time spent: ~ 2.5 hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "ps2\words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letters in secret_word:
        if letters in letters_guessed:
            continue
        else:
            return False

    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    displayWord = ""
    for letters in secret_word:
        if letters in letters_guessed:
            displayWord += letters
        else:
            displayWord += " _ "
    
    return displayWord



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    availableLetters = list(string.ascii_lowercase)
    for letters in letters_guessed:
        availableLetters.remove(letters)
    
    letterString = ''.join(availableLetters)
    return letterString


# def inputValidation(prompt):
#     '''
#     prompt: string of message to give the user when prompting for input
#     returns: string of singular lowercase letter
#     '''
#     while True:
#         try:
#             inputtedString = input(prompt)
#         # catches error in parsing
#         except ValueError:
#             print("Sorry, your input was invalid, try again.")
#             continue
#         # input is valid if its a single alphabetical letter
#         if inputtedString.isalpha() and len(inputtedString) == 1:
#             break
#         # otherwise still invalid
#         else:
#             print("Sorry, your input wasn't a single alphabetical letter, try again.")
#             continue
    
#     # returns the lowercase of the letter inputted
#     return inputtedString.lower()
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    print("Welcome to Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    guesses = 6
    warnings = 3
    vowels = "aeiou"
    uniqueString = ""

    while not is_word_guessed(secret_word, letters_guessed) and guesses > 0:
      if warnings < 0:
          warnings = 0
      print("-------------------------------------------------------------")
      print("You have", warnings, "warnings left.")
      print("You have", guesses, "guesses left.")
      print("Available letters:", get_available_letters(letters_guessed))

      # begin input validation
      while True:
        inputtedString = input("Please guess a letter: ")

        if inputtedString.isalpha() and len(inputtedString) == 1:
            break
        # otherwise still invalid
        else:
            print("Sorry, your input wasn't a single alphabetical letter, try again.")
            # if user has no warnings left subtract guesses
            if warnings <= 0:
                guesses -= 1
            warnings -= 1
            continue
    
      # makes userGuess the lowercase of the letter inputted
      userGuess = inputtedString.lower()

      # if letters not in the word
      if userGuess not in secret_word:
          # add guess to list of letters
          letters_guessed.append(userGuess)
          # one guess is used
          guesses -= 1
          # subtract another guess (total 2) for vowels
          if userGuess in vowels:
              guesses -= 1
            
          print("'" + userGuess + "' was not in the word: ", get_guessed_word(secret_word, letters_guessed))
      # otherwise if letters in the word and unguessed
      elif userGuess in secret_word and userGuess not in letters_guessed:
          # add guess to list of letters
          letters_guessed.append(userGuess)

          print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
      # otherwise the letter was already guessed
      else:
          # if user has no warnings left subtract guesses
          if (warnings <= 0):
              guesses -= 1
          warnings -= 1

          print("You've already guessed '" + userGuess + "', try again.")
    
    if guesses > 0:
        print("Congratulations, you win!")
        for letters in secret_word:
            if letters not in uniqueString:
                uniqueString += letters
        score = guesses * len(uniqueString)
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)




# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # strips all spaces, leaving only letters and underscores
    spacelessString = my_word.replace(" ", "")

    # continues if strings are equal in length
    if len(spacelessString) == len(other_word):
        # loops through each letter and compares
        for i in range(0, len(spacelessString)):
            # if string letter is the same as word letter or string letter is '_' continues
            if spacelessString[i] == other_word[i] or spacelessString[i] == '_':
                continue
            else:
                return False
    else:
        return False
    
    # can only reach this point if word matched as much as possible
    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matchesString = ""
    matches = 0
    for words in wordlist:
        if match_with_gaps(my_word, words):
            matchesString += words + " "
            matches += 1

    if len(matchesString) == 0:
        print("No matches found")
    else: 
        print(matchesString)
        print("\nThere was a total of", matches, "matches. All possible words are listed above.")



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    print("Welcome to Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    guesses = 6
    warnings = 3
    vowels = "aeiou"
    uniqueString = ""

    while not is_word_guessed(secret_word, letters_guessed) and guesses > 0:
      if warnings < 0:
          warnings = 0
      print("-------------------------------------------------------------")
      print("You have", warnings, "warnings left.")
      print("You have", guesses, "guesses left.")
      print("Available letters:", get_available_letters(letters_guessed))

      # begin input validation
      while True:
        inputtedString = input("Please guess a letter: ")

        if inputtedString.isalpha() and len(inputtedString) == 1 or inputtedString == "*":
            if inputtedString == "*":
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            break
        # otherwise still invalid
        else:
            print("Sorry, your input wasn't a single alphabetical letter, try again.")
            # if user has no warnings left subtract guesses
            if warnings <= 0:
                guesses -= 1
            warnings -= 1
            continue
    
      # makes userGuess the lowercase of the letter inputted
      userGuess = inputtedString.lower()

      # if they wanted a hint no need for below code
      if userGuess == "*":
          continue
      # if letters not in the word
      elif userGuess not in secret_word:
          # add guess to list of letters
          letters_guessed.append(userGuess)
          # one guess is used
          guesses -= 1
          # subtract another guess (total 2) for vowels
          if userGuess in vowels:
              guesses -= 1
            
          print("'" + userGuess + "' was not in the word: ", get_guessed_word(secret_word, letters_guessed))
      # otherwise if letters in the word and unguessed
      elif userGuess in secret_word and userGuess not in letters_guessed:
          # add guess to list of letters
          letters_guessed.append(userGuess)

          print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
      # otherwise the letter was already guessed
      else:
          # if user has no warnings left subtract guesses
          if (warnings <= 0):
              guesses -= 1
          warnings -= 1

          print("You've already guessed '" + userGuess + "', try again.")
    
    if guesses > 0:
        print("Congratulations, you win!")
        for letters in secret_word:
            if letters not in uniqueString:
                uniqueString += letters
        score = guesses * len(uniqueString)
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
