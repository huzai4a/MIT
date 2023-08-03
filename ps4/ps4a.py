# Problem Set 4A
# Name: Huzaifa Syed
# Collaborators: -
# Time Spent: 4-5 hrs
# Note: Don't fully understand recursion, got hints from pset sheet

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.

    '''

    # 1st base case - returns the singular character as a list
    if len(sequence) == 1:
        return [sequence]
    
    # separates the first character and makes
    # a remainder string
    remainder = sequence[1:]

    # does the recursive call for the smallPermList
    smallPermList = get_permutations(remainder)

    # creates an empty list of permutations
    permList = []
    # loops through each of shorter permutations
    for smallPerms in smallPermList:
        # adds all different ways first character of sequence can be
        # inserted into the -1 character permutations
        for i in range(len(sequence)):
            permutation = smallPerms[:i] + sequence[0] + smallPerms[i:]
            # prevents duplicates (just in case)
            if permutation not in permList:
                permList.append(permutation)

    return permList
    



    
    

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    example_input = "abc"
    print("Input: ", example_input)
    print("Expected output: ", "['abc', 'acb', 'bac', 'bca', 'cab', 'cba']")
    print("Actual Output: ", get_permutations(example_input))

    example_input = "xyz"
    print("Input: ", example_input)
    print("Expected output: ", "['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']")
    print("Actual Output: ", get_permutations(example_input))

    example_input = "bust"
    print("Input: ", example_input)
    print("Expected output: ", "['bust', 'buts', 'bsut', 'bstu', 'btsu', 'btus', 'ubst', 'ubts', 'usbt', 'ustb', 'utsb', 'utbs', 'sbut', 'sbtu', 'subt', 'sutb', 'stub', 'stbu', 'tbsu', 'tbus', 'tsbu', 'tsub', 'tusb', 'tubs']")
    print("Actual Output: ", get_permutations(example_input))

