from generate_gcode import gcode
import serial
import time

'''
You can do it this way or you can read in the
gcode from the gcode file and just loop through the list

You can also just use pronterface or some other printer control software if
you please
'''

comport = 'COM3'
baud_rate = 115200

ser = serial.Serial(comport, baud_rate, timeout=0)

ser.open()

time.sleep(4)

ser.reset_input_buffer()
ser.reset_output_buffer()

for line in gcode:
    
    while ser.readline() != 'ok\n':
        pass
    
    ser.write(line)
    
ser.close()