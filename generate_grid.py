def generate_grid(filename, width, height, debug = 0):
    
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P', \
                'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    newline = '\n'
    
    the_file = open(filename)
    characters = the_file.read()
    the_file.close()
    
    characters = list(characters)
    
    grid = []
    row = []
    prev_c = ' '
    
    for c in characters:
        
        #If non valid character
        if c not in alphabet and c != newline: 
            continue
        
        #If new line spotted
        elif c == newline:
            
            #If the first character is a return line
            if len(grid) == 0 and len(row) == 0: 
                continue
            
            #If two newlines in a row
            elif prev_c == newline: 
                prev_c = c
                continue
            
            #If new line is valid
            else: 
                prev_c = c
                grid.append(row)
                row = []
                
        else:
            prev_c = c
            row.append(c)
    
    if debug:
        print grid
        
    if len(grid) != height:
        print "You may be missing rows"
        print grid
        
    for i in grid:
        if len(i) != width:
            print "You have a row with an incorrect length"
            print i
            
    return grid