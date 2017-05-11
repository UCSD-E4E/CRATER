#!/usr/bin/env python
import os
import time
import random
import json
import numpy
import math
import serial
from socket import *
import scipy
from scipy import interpolate

#These are in percentages
matrix_R = numpy.matrix(

			'0   10   30   55    65    75   75   75   75   75   75;\
			 0   0    10   40    0     70    65    65    75   75   75;\
			 0   0    0    30    0     65    60    65    70    75   75;\
			 0   0    0    20    0     60    55    62.5    70    75   75;\
			 0   0    5    10    0     55    50    60    65    75   75;\
			 0   10   20   30    40    50    55    60    65    70    75;\
		     25  20   50   50    50    50    50    50    55    55    75;\
		     25  20   50   50    50    50    50    55    55    62.5    62.5;\
		     25  30   50   50    50    50    50    55    60    62.5    62.5;\
			 50  50   50   50    50    50    50    55    57.5    62.5    62.5;\
			 50  50   50   50    50    50    50    55    57.5    62.5    62.5'
			 
			 )
matrix_L = numpy.matrix('25   30   40   50   50    50    52    55    55    57.5    62.5;\
			 25   25   30   20   0     50    50    50    57.5    57.5    62.5;\
			 25   25   25   20   0     50    50    50    60    62.5    62.5;\
			 25   25   25   30   0     50    50    55    60    65    62.5;\
			 25   25   25   30   0     50    55    60    65    65    75;\
			 0    10   20   30   40    50    55    60    65    70    75;\
			 0    10   50   50   50    55    55    60    65    70    75;\
			 0    10   50   55   55    60    55    60    70    75   75;\
			 0    10   55   65   65    65    60    62.5    70    75   75;\
			 40   55   65   75  75   75   70    70    70    75   75;\
			 50   50   50   50   50    75   70    70    70    75   75')

inKsize = len(matrix_L)
outKsize = 101

kernelOut = numpy.zeros((outKsize, outKsize), numpy.uint8)

z_L = matrix_L
z_R = matrix_R

x_m = numpy.arange(11)
y_m = numpy.arange(11)

xx = numpy.linspace(x_m.min(), x_m.max(), outKsize)
yy = numpy.linspace(y_m.min(), y_m.max(), outKsize)

newKernel_L = interpolate.RectBivariateSpline(x_m, y_m, z_L)
matrix_L = newKernel_L(xx, yy)
newKernel_R = interpolate.RectBivariateSpline(x_m, y_m, z_R)
matrix_R = newKernel_R(xx, yy)
#print(matrix_L)
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
flagCruise = 0

logfile = open('/tmp/CRATER.log', 'w')

#2 = GPIO 18, 5 = GPIO 23
servoblasterfile = open('/dev/servoblaster', 'w')

def control_motor(data):
    x = data['X']
    y = data['Y']
    l = data['L']
    r = data['R']
    y_btn = data['Y_BTN']

    turn = data['TURN']

    global flag_t
    global flag
    global ticker
    global flagCruise
    global offsetR
    global offsetL

    if l == 1 and r == 0 and ticker > -5 and flag == 0:
	flag_t = time.time()
	flag = 1
	ticker = ticker - 1 
	
    elif r == 1 and l == 0 and ticker < 5 and flag == 0:
	flag_t = time.time()
	flag = 1
	ticker = ticker + 1

    if time.time() > flag_t + 1:
	flag = 0

 #   print(ticker)

    idx_x = math.floor((50*x) + 50)
    idx_y = math.floor((-50*y) + 50)

    #idx_x = math.floor((5*x) + 5)
    #idx_y = math.floor((-5*y) + 5)

    #50us corrections
    if ticker > 0 and flagCruise == 0: # Want more right, so add to left motor
	offsetL = ticker * 50
	offsetR = 0
    if ticker < 0 and flagCruise == 0: # Want more left, so add to right motor
	offsetR = ticker * -50
	offsetL = 0
    if ticker == 0:
	offsetL = 0
	offsetR = 0
    if y_btn == 1:
	ticker = 0
	offsetL = 0
	offsetR = 0
	flagCruise = 0

    if r == 1 and l == 1:
	flagCruise = 1
	offsetL = 130
	offsetR = 130
	ticker = 6

    if( turn == 1 )
    	offsetL = 180
    	offsetR = -180

    if( turn == 0 )
	offsetL = -180
	offsetR = 180

    pwmL = math.floor((matrix_L[idx_x, idx_y] / 100.0 * 1000 + 1000) + offsetL)
    pwmR = math.floor((matrix_R[idx_x, idx_y] / 100.0 * 1000 + 1000) + offsetR)

    #print("pwmL ", pwmL)
    #print("pwmR ", pwmR)

    pwmLmsg = '2=%dus\n' % pwmL
    pwmRmsg = '5=%dus\n' % pwmR
    servoblasterfile.write(pwmLmsg)
    print("%s\t\t%s\t\t%f\t%f"%(pwmLmsg[:-1], pwmRmsg[:-1], x, y))
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


