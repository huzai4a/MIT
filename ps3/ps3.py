# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

from pathlib import Path
import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

# added '*' as 0
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
WORDLIST_FILENAME = Path(__file__).with_name('words.txt')

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    # removes all spaces and makes word lowercase
    strippedString = word.lower().replace(" ", "")
    component1 = 0
    for letters in strippedString:
        component1 += SCRABBLE_LETTER_VALUES[letters]

    component2 = 7 * len(strippedString) - 3 * (n - len(strippedString))

    if component2 < 1:
        component2 = 1
 
    wordScore = component1*component2

    return wordScore


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for unused in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    

    # the -1 is due to the addition of the wildcard ( * ),
    # which is taking the place of a vowel
    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    # adds the wildcard in
    hand["*"] = 1
    
    # don't need any change here since the - 1 is taking
    # from the slots of num_vowels, not the ones after it
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    strippedString = word.lower().replace(" ", "")
    # copys the hand
    newHand = hand.copy()
    # for each letter in user's word
    for letters in strippedString:
        # if any letter is in the new hand
        if letters in newHand:
            # if that letter has a value of 1 remove it
            if newHand[letters] <= 1:
                newHand.pop(letters)
            # otherwise remove one from the new hand at key letters
            else:
                newHand[letters] -= 1
        # doesn't do anything if the letter isn't in the hand
    
    return newHand
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    
    # makes the string spaceless and lowercase
    strippedString = word.lower().replace(" ", "")
    tempHand = hand.copy()

    # continue wildcard validation if "*" is present
    if "*" in strippedString:
        # loops through to check each vowel case
        for i in range(len(VOWELS)):
            # if the wildcard replaced with any vowel
            # matches a word, string is valid
            if strippedString.replace("*", VOWELS[i]) in word_list:
                return True
        # if loop is completed, no word matches
        return False
    else:
        # continue validation if in word list
        if strippedString in word_list:
            # for each letter in the word
            for letters in strippedString:
                # if any letter is in the hand
                if letters in hand:
                    # remove 1 from tempHand
                    tempHand[letters] -= 1
                    # if there's a negative that means
                    # that too many of a letter was used
                    if tempHand[letters] < 0:
                        return False
                # otherwise letter was not in hand, invalid word
                else:
                    return False
        # otherwise is not a valid word from the list
        else:
            return False
    
    # if it passes all previous validation the word
    # is valid, return true
    return True

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    handLen = sum(hand.values())
    return handLen

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # initialize score as an int
    tempScore = 0
    # the hand is copied so as to not alter the original hand
    tempHand = hand.copy()

    while len(tempHand) > 0:
        print("Current hand:", end=" ")
        display_hand(tempHand)

        inputtedString = input("Enter a word, or \"!!\" to indicate that you are finished: ")

        if inputtedString == "!!":
            break
        else:
            if is_valid_word(inputtedString, tempHand, word_list):
                tempScore += get_word_score(inputtedString, calculate_handlen(tempHand))
                print("\"" + inputtedString + "\" earned", get_word_score(inputtedString, calculate_handlen(tempHand)), "points. Total:", tempScore, "points")
            else:
                print("'" + inputtedString + "' is not a valid word.")

        tempHand = update_hand(tempHand, inputtedString)
    
    # Tells the user they ran out of letters if hand is empty
    if len(tempHand) <= 0:
        print("Ran out of letters.", end=" ")
            
    # prints the total score regardless of end case
    print("Total score of this hand:", tempScore, "points")

    # returns the score from the current hand
    return tempScore



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    # if the letter's not in the hand, it remains the same
    if not(letter in hand):
        pass
    else:
       while True:
           randomLetter = random.choice(VOWELS+CONSONANTS)
           # if the random letter isn't in the hand and is different from
           # the old letter, replace the key and break from while
           if not (randomLetter in hand) and not (randomLetter == letter):
               hand[randomLetter] = hand.pop(letter)
               break
    
    return hand
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    # initializing totalScore variable
    totalScore = 0
    # starts as false so that user is asked for replay and substitute
    replayed = False
    substituted = False
    # gets a number of hands to play
    numOfHands = validInt("Enter total number of hands: ")
    
    # continues while the chosen number of hands hasn't been played
    while numOfHands > 0:
        # gets a new hand and displays it
        tempHand = deal_hand(HAND_SIZE)
        print("Current hand:", end=" ")
        display_hand(tempHand)

        # if substitution has already been used then nothing needs to be done
        if substituted:
            pass
        else:
            # begins input validation for substituting a letter
            subChoice = yesOrNo("Would you like to substitute a letter? ")
            if subChoice == "yes":
                # gets letter to replace and replaces it in hand
                replaceLet = validLetter("What letter would you like to replace? ")
                tempHand = substitute_hand(tempHand, replaceLet)
                substituted = True
            # otherwise the user says no it prints an empty line and leaves loop
            else:
                print()

        # plays the game and stores hand score
        handScore = play_hand(tempHand, word_list)
        # separates the current hand playthrough and the following messages
        print("-----------------")

        # if it has already been replayed, pass
        if replayed:
            pass
        # otherwise begin replay validation
        else:
            # asks user if they would like to replay
            replayChoice = yesOrNo("Would you like to replay this hand? You only get this option once. ")
            # if they want to replay, the game restarts with the same hand
            if replayChoice == "yes":
                replayScore = play_hand(tempHand, word_list)
                # keeps the greater of the two scores
                if replayScore > handScore:
                    handScore = replayScore
                # this makes the user unable to replay again
                replayed = True
            # otherwise it passes
            else:
                pass

            # adds the score from the current hand to the total
            totalScore += handScore
            numOfHands -= 1
    
    print("Total score over all hands:", totalScore)

def validLetter(prompt):
    """
    prompt: string of message to give the user when prompting for input
    returns: valid singular letter
    """
    while True:
        userInput = input(prompt)
        if len(userInput) > 1: # and userInput.isalpha()
            print("Invalid input. Please enter a singular letter")
        else:
            return userInput



def validInt(prompt):        
    """
    prompt: string of message to give the user when prompting for input
    returns: valid integer
    """
    while True:
        userInput = input(prompt)

        if userInput.isdigit():
            return int(userInput)
        else:
            print("Invalid number, make sure to enter an integer.")

def yesOrNo(prompt):
    """
    prompt: string of message to give the user when prompting for input
    returns: string of "yes" or "no"
    """
    while True:
        userString = input(prompt)

        if not(userString == "yes") and not(userString == "no"):
            print("Invalid input, say yes or no.")
        else:
            return userString

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
