from generate_grid import generate_grid
from generate_words import generate_words

width = 14 #in words
height = 14 #in words

class Solver():
    
    def __init__(self, puzzle_filename, words_filename):
        self.width = 14 #in words
        self.height = 14 #in words
        
        self.grid = generate_grid(puzzle_filename, self.width, self.height)
        self.words = generate_words(words_filename)
        
        self.words.sort()
        
        self.word_dict = {}
        
        #Creates word bank dictionaries
        #One set (index 0) is for the words as they are
        #Set two (index 1) are the same words reversed
        
        #('S', 0) will contain {'SQUEEZE', 'SHORT'}
        #{'S', 1} will contain {'SKCOS', 'SANANAB'}
        
        for word in self.words: 
            rev_word = word[::-1]
            
            if (word[0],0) not in self.word_dict:
                self.word_dict[(word[0], 0)] = [word]
            elif (word[0],0) in self.word_dict:
                prev_list = self.word_dict[(word[0],0)]
                prev_list.append(word)
                
                self.word_dict[(word[0],0)] = prev_list
                
            if (word[-1],-1) not in self.word_dict:
                self.word_dict[(word[-1], -1)] = [rev_word]
                
            elif (word[-1],-1) in self.word_dict:
                prev_list = self.word_dict[(word[-1],-1)]
                prev_list.append(rev_word)
                self.word_dict[(word[-1],-1)] = prev_list
        
    def is_valid_pos(self, row, col):
        
        if col < 0 or row < 0 or col >= width or row >= height:
            return False
        else:
            return True
    
    def get_successors(self, row, col, direction, path, interm_word):
        successors = []
        '''
        Direction encoding:
        
        Right = 0
        Down Right = 1
        Down = 2
        Down Left = 3
        
        With no direction in mind, we check all possible successors if the positions are valid.
        If a direction is specified we only check successors in that direction
        '''
        
        if direction == None:
            if self.is_valid_pos(row, col + 1):
                spath = path[:]
                spath.append((row, col + 1))
                successors.append((row, col + 1, 0, spath, interm_word + self.grid[row][col + 1]))
            if self.is_valid_pos(row + 1, col + 1):
                spath = path[:]
                spath.append((row + 1, col + 1))
                successors.append((row + 1, col + 1, 1, spath, interm_word + self.grid[row + 1][col + 1]))
            if self.is_valid_pos(row + 1, col):
                spath = path[:]
                spath.append((row + 1, col))
                successors.append((row + 1, col, 2, spath, interm_word + self.grid[row + 1][col]))
            if self.is_valid_pos(row + 1, col - 1):
                spath = path[:]
                spath.append((row + 1, col - 1))
                successors.append((row + 1, col - 1, 3, spath, interm_word + self.grid[row + 1][col - 1]))
            return successors
        
        elif direction == 0 and self.is_valid_pos(row, col + 1):
            path.append((row, col + 1))
            successors.append((row, col + 1, 0, path, interm_word + self.grid[row][col + 1]))
            return successors
                
        elif direction == 1 and self.is_valid_pos(row + 1, col + 1):
            path.append((row + 1, col + 1))
            successors.append((row + 1, col + 1, 1, path, interm_word + self.grid[row + 1][col + 1]))
            return successors
        
        elif direction == 2 and self.is_valid_pos(row + 1, col):
            path.append((row + 1, col))
            successors.append((row + 1, col, 2, path, interm_word + self.grid[row + 1][col]))
            return successors
        
        elif direction == 3 and self.is_valid_pos(row + 1, col - 1):
            path.append((row + 1, col - 1))
            successors.append((row + 1, col - 1, 3, path, interm_word + self.grid[row + 1][col - 1]))
            return successors
            
        return successors
    
    def check_successors(self, row, col, directions, path, letter):
        #Runs a depth-first search for each sucessor of the supplied node
        result = False
        
        successors = self.get_successors(row, col, directions, path, letter)
        
        while successors != []:
            node_list = []
            for s in successors:
                node_list.append(self.grid[s[0]][s[1]])
      
            s = successors.pop()
      
            interm_word = s[-1]
            if (interm_word[0], 0) in self.word_dict:
                for word in self.word_dict[(interm_word[0],0)]:
                    if interm_word in word and interm_word != word:
                        for succ in self.get_successors(s[0], s[1], s[2], s[3], s[4]):
                            successors.append(succ)
                        break
                        
                    elif interm_word in word and interm_word == word:
                        if result == False:
                            result = [s[3]]
                        elif s[3] not in result:
                                result.append(s[3])
                            
            if (interm_word[0], -1) in self.word_dict:
                for word in self.word_dict[(interm_word[0],-1)]:
                    if interm_word in word and interm_word != word:
                        for succ in self.get_successors(s[0], s[1], s[2], s[3], s[4]):
                            successors.append(succ)
                        break
                        
                    elif interm_word in word and interm_word == word:
                        if result == False:
                            result = [s[3]]
                        elif s[3] not in result:
                                result.append(s[3])   
        
        return result
    
    
    def solve(self):
        #Loop through all nodes
        paths = []
        
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                    
                letter = self.grid[row][col]
                    
                if (letter, 0) in self.word_dict or (letter, -1) in self.word_dict:
                    
                    result = self.check_successors(row, col, None, [(row, col)], letter)
                    if result == False:
                        continue
                    else:
                        for res in result:
                            paths.append(res)
        
        #Fixes a bug in the implementation where
        #Sometimes a word will begin with 2 letters that are also
        #The end of another word i.e. MUFFIN and PLUM
        for path in paths:                
            seen = {}
            for node in path[:]:
                if node not in seen:
                    seen[node] = 1
                else:
                    path.remove(node)
                    
        return paths