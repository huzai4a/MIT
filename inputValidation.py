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