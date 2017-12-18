def generate_words(filename):
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P', \
                'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    newline = '\n'
    
    the_file = open(filename)
    characters = the_file.read()
    characters = list(characters)
    the_file.close()
    
    words = []
    word = []
    
    for c in characters:
        
        if c in alphabet:
            word.append(c)
        
        if c == newline and len(word) != 0:
            words.append(''.join(word))
            word = []

    return words