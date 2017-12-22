puzzle_filename = 'puzzle.txt'
words_filename = 'words.txt'

origin_x = 0 #Origin for 3D printer toolhead
origin_y = 65
writing_height = 1.0 #Z height for toolhead in mm

#Spacing between centroids of letters on puzzle
x_spacing = 7.7 #in mm
y_spacing = 11.35 #in mm

#offset from top-left corner of box around puzzle
x_offset = 6 #in mm
y_offset = 6.7 #in mm

#Distance from centroid of letter for boxing in words
margin = 3 #in mm

#For diagonal boxes
dxmargin = 4.5 #in mm
dymargin = dxmargin*x_spacing/y_spacing + 0.5 #in mm

feedrate = 30 # in mm per second