from solve import Solver
import matplotlib.pyplot as plt
import math

puzzle_filename = 'puzzle.txt'
words_filename = 'words.txt'

origin_x = 0
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

origin = (origin_x, origin_y) #3D Printer coordinates of top left corner of page in mm

#For g-code moves that go up and down
up = 'Z5.0'
down = 'Z' + str(writing_height)
endl = '\n'

def quicker_move(line):
    return 'G0 F10500 X' + line.split('X')[-1]

def go_up(line):
    
    if 'Z' in line:
        return line.split('Z')[0] + up + endl
    else:
        return line.split(endl)[0] + ' ' + up + endl

def go_down(line):
    
    if 'Z' in line:
        return line.split('Z')[0] + down + endl
    else:
        return line.split(endl)[0] + ' ' + down + endl

def go_to(state):
    return 'G1 F' + str(feedrate*60) + ' X' + str(state[0]) + ' Y' + str(state[1]) + endl

def rotate_about_origin(x, y):
    x_r = -y
    y_r = x
    return (x_r, y_r)

def index_to_mm(state):
    x_coor = x_offset + (state[1]) *x_spacing
    y_coor = - y_offset - (state[0]) *y_spacing

    return x_coor, y_coor

def determine_angle_n_dir(p1, p2):
    '''
    Direction encoding:
    
    Right = 0
    Down Right = 1
    Down = 2
    Down Left = 3
    '''
    
    dy = float(p2[0]-p1[0])
    dx = p2[1]-p1[1]
    
    if dx == 0:
        return math.radians(270), 2
    elif dy == 0:
        return 0, 0
    elif dy > 0 and dx < 0:
        return math.atan2(dy, dx), 3
    elif dy > 0 and dx > 0:
        return math.atan2(dy, dx), 1
    
def create_word_loop(path):
    #Generates box around word
    
    '''
    Direction encoding:
    
    Right = 0
    Down Right = 1
    Down = 2
    Down Left = 3
    '''
    
    loop = []
    
    angle, direction = determine_angle_n_dir(path[0], path[1])
    
    if direction == 0:
        s_x_coor, s_y_coor = index_to_mm(path[0])
        e_x_coor, e_y_coor = index_to_mm(path[-1])
        
        loop.append(go_to((s_x_coor, s_y_coor)))
        loop.append(go_to((s_x_coor - margin, s_y_coor + margin)))
        loop.append(go_down(loop[-1]))
        loop.append(go_to((s_x_coor - margin, s_y_coor - margin)))
        loop.append(go_to((e_x_coor + margin, e_y_coor - margin)))
        loop.append(go_to((e_x_coor + margin, e_y_coor + margin)))
        loop.append(go_to((s_x_coor - margin, s_y_coor + margin)))
        
        return loop
    
    elif direction == 1:
        s_x_coor, s_y_coor = index_to_mm(path[0])
        e_x_coor, e_y_coor = index_to_mm(path[-1])
        
        loop.append(go_to((s_x_coor, s_y_coor)))
        loop.append(go_to((s_x_coor - dxmargin, s_y_coor)))
        loop.append(go_down(loop[-1]))
        loop.append(go_to((e_x_coor, e_y_coor - dymargin)))
        loop.append(go_to((e_x_coor + dxmargin, e_y_coor)))
        loop.append(go_to((s_x_coor, s_y_coor + dymargin)))
        loop.append(go_to((s_x_coor - dxmargin, s_y_coor)))
        
        return loop
    
    elif direction == 2:
        s_x_coor, s_y_coor = index_to_mm(path[0])
        e_x_coor, e_y_coor = index_to_mm(path[-1])
        
        loop.append(go_to((s_x_coor, s_y_coor)))
        loop.append(go_to((s_x_coor - margin, s_y_coor + margin)))
        loop.append(go_down(loop[-1]))
        loop.append(go_to((e_x_coor - margin, e_y_coor - margin)))
        loop.append(go_to((e_x_coor + margin, e_y_coor - margin)))
        loop.append(go_to((s_x_coor + margin, s_y_coor + margin)))
        loop.append(go_to((s_x_coor - margin, s_y_coor + margin)))
        
        return loop
    
    elif direction == 3:
        s_x_coor, s_y_coor = index_to_mm(path[0])
        e_x_coor, e_y_coor = index_to_mm(path[-1])
        
        loop.append(go_to((s_x_coor, s_y_coor)))
        loop.append(go_to((s_x_coor, s_y_coor + dymargin)))
        loop.append(go_down(loop[-1]))
        loop.append(go_to((e_x_coor - dxmargin, e_y_coor)))
        loop.append(go_to((e_x_coor, e_y_coor - dymargin)))
        loop.append(go_to((s_x_coor + dxmargin, s_y_coor)))
        loop.append(go_to((s_x_coor, s_y_coor + dymargin)))
        
        return loop

def connect_loops(loops):
    connected_loops = []
    for loop in loops:
        connected_loops.append(go_up(quicker_move(loop[0])))
        for line in loop:
            if line == loop[0]:
                continue
            else:
                connected_loops.append(line)

    return connected_loops

def rotate_gcode(gcode):
    #Rotates gcode because in my setup I need
    #to rotate the page 90 degrees on the 3D
    #printer build plate
    
    rot_gcode = []
    
    for line in gcode[1::]:
        x, y = get_coordinates(line)
        xr, yr = rotate_about_origin(x, y)
        
        xr += origin_x
        yr += origin_y
        
        r_line = go_to((xr, yr))
        if 'Z' not in line:
            rot_gcode.append(r_line)
        else:
            if float(line.split('Z')[1].split('\n')[0]) > writing_height:
                rot_gcode.append(go_up(r_line))
            else:
                rot_gcode.append(go_down(r_line))
                
    rot_gcode.insert(0, gcode[0])
    rot_gcode.append('G1 F1200 X0 Y175 Z125\n')
    return rot_gcode

def generate_gcode(paths):
    #Generates list of all gcode
    
    loops = []
    for path in paths:
        loops.append(create_word_loop(path))
    
    gcode = connect_loops(loops)
    gcode.insert(0, 'G28\n')
    return gcode

def get_coordinates(line):
    x = float(line.split('X')[1].split(' ')[0])
    y = float(line.split('Y')[1].split(' ')[0])
    
    return x, y
    
def get_all_coordinates(gcode):
    xc = []
    yc = []
    for line in gcode:
        if 'X' in line:
            xc.append(float(line.split('X')[1].split(' ')[0]))
        if 'Y' in line:
            yc.append(float(line.split('Y')[1].split(' ')[0]))
            
    return xc, yc

#########################

#And now to actually generate gcode
    
#First solve the puzzle
solver = Solver(puzzle_filename, words_filename)
paths = solver.solve()

#Generate and rotate gcode
gcode = generate_gcode(paths)
gcode = rotate_gcode(gcode)

#Write gcode file
gcode_file = open("puzzle.gcode","w+")
for line in gcode:
    gcode_file.write(line)
    
gcode_file.close()

#Plot
xc, yc = get_all_coordinates(gcode)

plt.figure(figsize=(y_spacing, x_spacing))
plt.plot(xc, yc)
plt.xlim(origin_x, origin_x + 162) #162 and 112 are dimensions of the box
plt.ylim(origin_y, origin_y + 112) #Around the puzzle in mm
plt.show()
