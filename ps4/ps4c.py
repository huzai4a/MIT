# Problem Set 4C
# Name: Huzaifa Syed
# Collaborators: -
# Time Spent: 2 hrs

from pathlib import Path
import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = Path(__file__).with_name('words.txt')

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        
        return self.message_text
    
    def set_message_text(self, text):
        '''
        Used to safely set self.message_text outside of the class
        
        Returns: none
        '''
        self.message_text = text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        # note to self: the vowels_permutation string can only be 
        # a rearranged version of the vowels, thats all it is

        # the dictionary to be returned
        letterDict = {}
        # for each vowel
        for i in range(len(VOWELS_LOWER)):
            # sets the corresponding vowel to the provided letters in corresponding order
            letterDict[VOWELS_LOWER[i]] = vowels_permutation[i]
            letterDict[VOWELS_UPPER[i]] = vowels_permutation[i].upper()
        
        # assigns all non-vowels to themselves
        for letters in CONSONANTS_LOWER:
            letterDict[letters] = letters
            letterDict[letters.upper()] = letters.upper()
        
        return letterDict

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        # initializes list to hold each letter
        appliedTranspose = []
        # for each character in the message
        for letters in self.get_message_text():
            # if the character is alphabetical add its 
            # corresponding letter from the dictionary
            if letters.isalpha():
                appliedTranspose.append(transpose_dict[letters])
            # otherwise add the character itself
            else:
                appliedTranspose.append(letters)

        # returns a string by joining the appliedTranspose list
        return ''.join(appliedTranspose)
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        
        # creates a list of all permutations of the vowels
        vowelPermList = get_permutations(VOWELS_LOWER)
        # initializes the integers needed for bests
        bestCount = 0
        bestIndex = 0
        # stores the original message to decode
        originalText = self.get_message_text()
        # creates list where words will be validated
        tempDecrypt = []

        for permutations in vowelPermList:
            # resets count to 0 each loopthrough
            wordCounter = 0
            # creates new dictionary based on new permutation of vowels
            tempDict = self.build_transpose_dict(permutations)

            # fills list with 'decrypted' words from message
            tempDecrypt = self.apply_transpose(tempDict).split(" ")

            # for each word in decrypted list
            for words in tempDecrypt:
                # if the word is valid add to count
                if is_word(self.get_valid_words(), words):
                    wordCounter += 1
            
            # if there are more words than the current best decryption,
            # there shall be a new best decryption
            if wordCounter > bestCount:
                bestCount = wordCounter
                bestIndex = vowelPermList.index(permutations)

            # at the end of each loop reset the message to its original encryption
            self.set_message_text(originalText)

        # if the word count is 0 no permutations worked; send back original string
        if bestCount == 0:
            return self.get_message_text()
        else:
            # creates new dictionary based on vowel permutation
            # that formed the most words
            tempDict = self.build_transpose_dict(vowelPermList[bestIndex])
            return self.apply_transpose(tempDict)




    

if __name__ == '__main__':

    # Example test case
    # message = SubMessage("Hello World!")
    # permutation = "eaiuo"
    # enc_dict = message.build_transpose_dict(permutation)
    # print("Original message:", message.get_message_text(), "Permutation:", permutation)
    # print("Expected encryption:", "Hallu Wurld!")
    # print("Actual encryption:", message.apply_transpose(enc_dict))
    # enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    # print("Decrypted message:", enc_message.decrypt_message())
     
    # SubMessage test case 1
    message1 = SubMessage("Crazy? I was crazy once.")
    permutation1 = "uoiea"
    #              "aeiou"
    enc_dict = message1.build_transpose_dict(permutation1)
    print("Original message:", message1.get_message_text(), "Permutation:", permutation1)
    print("Expected encryption:", "Cruzy? I wus cruzy enco.")
    print("Actual encryption:", message1.apply_transpose(enc_dict))
    # SubMessage test case 2
    message2 = SubMessage("The quick brown fox jumped over a lazy dog.")
    permutation2 = "oieua"
    #              "aeiou"
    enc_dict = message2.build_transpose_dict(permutation2)
    print("Original message:", message2.get_message_text(), "Permutation:", permutation2)
    print("Expected encryption:", "Thi qaeck bruwn fux jampid uvir o lozy dug.")
    print("Actual encryption:", message2.apply_transpose(enc_dict))

    # EncryptedSubMessage test case 1
    enc_message = EncryptedSubMessage("Qoeck santanca fur tast cisa.")
    print("Input message:", enc_message.get_message_text())
    print("Expected decryption:", "Quick sentence for test case.")
    print("Decrypted message:", enc_message.decrypt_message())
    # EncryptedSubMessage test case 2
    enc_message2 = EncryptedSubMessage("Hulla, O jest fonoshud hogh schaal!")
    print("Input message:", enc_message2.get_message_text())
    print("Expected decryption:", "Hello, I just finished high school!")
    print("Decrypted message:", enc_message2.decrypt_message())

# test 1
# Quick sentence for test case.
# Qoeck santanca fur tast cisa.
# iaeuo
# aeiou
# test 2
# Hello, I just finished high school!
# Hulla, O jest fonoshud hogh schaal!
# iuoae
# aeiou