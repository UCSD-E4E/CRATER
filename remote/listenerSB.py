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

inKsize = len(matrix_L)
outKsize = 101

kernelOut = numpy.zeros((outKsize, outKsize), numpy.uint8)

z_L = matrix_L
z_R = matrix_R

x = numpy.arange(11)
y = numpy.arange(11)

xx = numpy.linspace(x.min(), x.max(), outKsize)
yy = numpy.linspace(y.min(), y.max(), outKsize)

newKernel_L = interpolate.RectBivariateSpline(x, y, z_L)
matrix_L = newKernel_L(xx, yy)
newKernel_R = interpolate.RectBivariateSpline(x, y, z_R)
matrix_R = newKernel_R(xx, yy)
print(matrix_L)
# os.system('sudo ./servod --min=1000us --max=2000us --p1pins=0,0,12,0,0,16')
# Left motor = 2
# Right motor = 5

#Set up the serial communication port
#ser = serial.Serial('/dev/ttyACM0', 9600)

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',12000))

ticker = 0
flag = 0
flag_t = 0
offsetR = 0
offsetL = 0

logfile = open('/tmp/CRATER.log', 'w')

#2 = GPIO 18, 5 = GPIO 23
servoblasterfile = open('/dev/servoblaster', 'w')

def control_motor(data):
    x = data['X']
    y = data['Y']
    l = data['L']
    r = data['R']
    y = data['Y_BTN']
    global flag_t
    global flag
    global ticker

    if l == 1 and ticker > -5 and flag == 0:
	flag_t = time.time()
	flag = 1
	ticker = ticker - 1 
	
    if r == 1 and ticker < 5 and flag == 0:
	flag_t = time.time()
	flag = 1
	ticker = ticker + 1

    if time.time() > flag_t + 1:
	flag = 0

    print(ticker)

    idx_x = math.floor((50*x) + 50)
    idx_y = math.floor((-50*y) + 50)

    #50us corrections
    if ticker > 0: # Want more right, so add to left motor
	offsetL = ticker * 50
	offsetR = 0
    if ticker < 0: # Want more left, so dd to right motor
	offsetR = ticker * 50
	offsetL = 0
    if ticker == 0:
	offsetL = 0
	offsetR = 0
    if y == 1:
	ticker = 0
	offsetL = 0
	offsetR = 0

    pwmL = math.floor((matrix_L[idx_x, idx_y] / 100.0 * 1000 + 1000) + offsetL)
    pwmR = math.floor((matrix_R[idx_x, idx_y] / 100.0 * 1000 + 1000) + offsetR)

    print("pwmL ", pwmL)
    print("pwmR ", pwmR)

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

    a = data['A_BTN']
    b = data['B_BTN']
    x = data['X_BTN']
    y = data['Y_BTN']
    
    command = 'POLLING'
    
    #Open All Valves
    if ( a == 1 and b == 0 and x == 1 and y == 0 ):
        command = 'A'
        ser.write(command)
        print('Open All Valves')
    
    #Close All Valves & Reset Counter
    elif ( a == 0 and b == 1 and x == 0 and y == 1 ):
        command = 'R'
        ser.write(command)
        print('Close All Valves and Reset')
    
    #Open Next Valve
    elif ( a == 1 and b == 0 and x == 0 and y == 0 ):
        command = 'N'
        ser.write(command)
        print('Open Next Valve')



def main():
    while True:
        message, address = serverSocket.recvfrom(1024)
        message = message.upper()

        #print(message)
        data = json.loads(message)
	#print(data['L'])     
        control_motor(data)
        control_payload(data)

if __name__=='__main__':
    main()


