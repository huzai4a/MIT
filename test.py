VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'
def build_transpose_dict(vowels_permutation):
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

print(build_transpose_dict("wjvru"))