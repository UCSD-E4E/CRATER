#!/usr/bin/env python
import os
import time
import random
import json
import numpy
import math
import serial
from socket import *

# These are now in percentages
matrix_R = numpy.matrix('0   10   30   60    80    100   100   100   100   100   100;\
			 0   0    10   40    0     90    80    80    100   100   100;\
			 0   0    0    30    0     80    70    80    90    100   100;\
			 0   0    0    20    0     70    60    75    90    100   100;\
			 0   0    5    10    0     60    50    70    80    100   100;\
			 0   10   20   30    40    50    60    70    80    90    100;\
		         25  20   50   50    50    50    50    50    55    60    100;\
		         25  20   50   50    50    50    50    60    60    75    75;\
		         25  30   50   50    50    50    50    60    70    75    75;\
			 50  50   50   50    50    50    50    55    65    75    75;\
			 50  50   50   50    50    50    50    55    65    75    75')

matrix_L = numpy.matrix('25   30   40   50   50    50    55    60    60    65    75;\
			 25   25   30   20   0     50    50    50    65    65    75;\
			 25   25   25   20   0     50    50    50    70    75    75;\
			 25   25   25   30   0     50    50    60    70    80    75;\
			 25   25   25   30   0     50    60    70    80    80    100;\
			 0    10   20   30   40    50    60    70    80    90    100;\
			 0    10   50   50   50    60    60    70    80    90    100;\
			 0    10   50   60   60    70    60    70    90    100   100;\
			 0    10   60   80   80    80    70    75    90    100   100;\
			 40   60   80   100  100   100   90    90    90    100   100;\
			 50   50   50   50   50    100   90    90    90    100   100')

# os.system('sudo ./servod --min=1000us --max=2000us --p1pins=0,0,12,0,0,16')
# Left motor = 2
# Right motor = 5

#Set up the serial communication port
#ser = serial.Serial('/dev/ttyACM0', 9600)

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',12000))

logfile = open('/tmp/CRATER.log', 'w')

#2 = GPIO 18, 5 = GPIO 23
servoblasterfile = open('/dev/servoblaster', 'w')

def control_motor(data):
    x = data['X']
    y = data['Y']

    idx_x = math.floor((5*x) + 5)
    idx_y = math.floor((-5*y) + 5)

    pwmL = matrix_L[idx_x, idx_y] / 100.0 * 1000 + 1000
    pwmR = matrix_R[idx_x, idx_y] / 100.0 * 1000 + 1000

    pwmLmsg = '2=%dus\n' % pwmL
    pwmRmsg = '5=%dus\n' % pwmR
    servoblasterfile.write(pwmLmsg)
    logfile.write(pwmLmsg)
    logfile.flush()
    servoblasterfile.flush()
    servoblasterfile.write(pwmRmsg)
    servoblasterfile.flush()
    time.sleep(0.02)

def control_payload(data):
    a = data['A']

    if( a == 1 ):
        command = 'H'
    else:
        command = 'L'

    #ser.write(command)

    #if command == 'H':
        #print('Led on')
    #elif command == 'L':
        #print('Led off')

def main():
    while True:
        message, address = serverSocket.recvfrom(1024)
        message = message.upper()

        print(message)

        data = json.loads(message)
        control_motor(data)
        control_payload(data)

if __name__=='__main__':
    main()


