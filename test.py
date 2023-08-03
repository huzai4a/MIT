import string
def build_shift_dict(shift):
    '''
    Creates a dictionary that can be used to apply a cipher to a letter.
    The dictionary maps every uppercase and lowercase letter to a
    character shifted down the alphabet by the input shift. The dictionary
    should have 52 keys of all the uppercase letters and all the lowercase
    letters only.        
    
    shift (integer): the amount by which to shift every letter of the 
    alphabet. 0 <= shift < 26

    Returns: a dictionary mapping a letter (string) to 
                another letter (string). 
    '''
    
    # initializes the dictionary
    shiftedDict = {}
    # note: I realized the *2 from looking online after 
    # feeling my method was inefficient
    lowerAlpha = string.ascii_lowercase*2
    upperAlpha = string. ascii_uppercase*2

    # shifts each lowercase, adding to dictionary
    for letters in lowerAlpha:
        shiftedDict[letters] = lowerAlpha[lowerAlpha.index(letters) + shift]
    # shifts each lowercase, adding to dictionary
    for letters in upperAlpha:
        shiftedDict[letters] = upperAlpha[upperAlpha.index(letters) + shift]

    return shiftedDict


def apply_shift(message_text, shift):
    '''
    Applies the Caesar Cipher to self.message_text with the input shift.
    Creates a new string that is self.message_text shifted down the
    alphabet by some number of characters determined by the input shift        
    
    shift (integer): the shift with which to encrypt the message.
    0 <= shift < 26

    Returns: the message text (string) in which every character is shifted
            down the alphabet by the input shift
    '''

    # initialize dictionary and codedMessage string
    shiftedDict = build_shift_dict(shift)
    codedMessage = []

    for letters in message_text:
        # if letter is alphabetical, shift
        if letters.isalpha():
            codedMessage.append(shiftedDict[letters])
        # otherwise character was non-alphabetical, skip it
        else:
            codedMessage.append(letters)
            continue

    return ''.join(codedMessage)

print(apply_shift("Hello World!", 4))