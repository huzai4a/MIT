import string
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

class PhraseTrigger (Trigger):
    def __init__(self, phrase):
        """
        Initializes a PhaseTrigger object

        phrase (string): The phrase to use for the trigger

        A PhraseTrigger has one attribute:
            self.phrase (string, determined by input text)
        """

        self.phrase = phrase.lower()

    def in_text(self, text):
        """
        Checks whether self.phrase is in the inputted text

        Returns: True or False
        """

        tempString = text.lower()

        for puncs in string.punctuation:
            # each punctuation is replaced with a space
            # note: strings are immutable, this is inefficient
            tempString.replace(puncs, " ")
            
        # splits tempString into list of words
        strippedWords = tempString.split(" ")
        # splits the phrase into a list of words
        splitPhrase = self.phrase.split(" ")

        # if any of the phrase words aren't in the list, there's no match
        if splitPhrase[0] not in strippedWords:
            return False
        # otherwise there could be a match
        else:
            # for each word in the given text
            for textWords in strippedWords:
                # if any word is the first word of our phrase
                if textWords == splitPhrase[0]:
                    # get this words index and begin checking the rest of the phrase
                    index = strippedWords.index(textWords)
                    # start a loop count at 1, so as to check the 2nd element of splitPhrase first
                    for i in range(1, len(splitPhrase)):
                        index += 1
                        if splitPhrase[i] == strippedWords[index]:
                            # if the last word of the phrase string has been reached
                            # the full phrase is in the text
                            if (i+1) == len(splitPhrase):
                                return True
            
            # if this point is reached there was no matches
            return False
        
ny = PhraseTrigger("new yoRk")

print(ny.in_text("Jeff Bezos New York Becomes the Richest Person in"))