#!/usr/bin/env python

import random
from socket import *
import json
import RPi.GPIO as IO
import time
import numpy
import math
import serial

matrix_R = numpy.matrix('10   11   13   16    18    20    20    20    20    20   20;\
			 10   10   11   14    0     19    18    18    20    20   20;\
			 10   10   10   13    0     18    17    18    19    20   20;\
			 10   10   10   12    0     17    16    17.5  19    20   20;\
			 10   10   10.5 11    0     16    15    17    18    20   20;\
			 10   11   12   13    14    15    16    17    18    19   20;\
		         12.5 12   15   15    15    15    15    15    15.5  16   20;\
		         12.5 12   15   15    15    15    15    16    16    17.5 17.5;\
		         12.5 13   15   15    15    15    15    16    17    17.5 17.5;\
			 15   15   15   15    15    15    15    15.5  16.5  17.5 17.5;\
			 15   15   15   15    15    15    15    15.5  16.5  17.5 17.5')

matrix_L = numpy.matrix('12.5 13   14   15    15    15    15.5  16    16    16.5 17.5;\
			 12.5 12.5 13   12    0     15    15    15    16.5  16.5 17.5;\
			 12.5 12.5 12.5 12    0     15    15    15    17    17.5 17.5;\
			 12.5 12.5 12.5 13    0     15    15    16    17    18   17.5;\
			 12.5 12.5 12.5 13    0     15    16    17    18    18   20;\
			 10   11   12   13    14    15    16    17    18    19   20;\
			 10   11   15   15    15    16    16    17    18    19   20;\
			 10   11   15   16    16    17    16    17    19    20   20;\
			 10   11   16   18    18    18    17    17.5  19    20   20;\
			 14   16   18   20    20    20    19    19    19    20   20;\
			 15   15   15   15    15    20    19    19    19    20   20')

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(23,IO.OUT)
IO.setup(17,IO.OUT)

right_motor = IO.PWM(23,100)
left_motor = IO.PWM(17,100)

right_motor.start(0)
left_motor.start(0)

#Set up the serial communication port
#ser = serial.Serial('/dev/ttyACM0', 9600)

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',12000))
                                                   
def control_motor(data):
	x = data['X']
	y = data['Y']

	pwmx = (5 * x) + 15
	pwmy = (-5 * y) + 15
	pwmL = 15
	pwmR = 15

	idx_x = math.floor((5 * x) + 5)
	idx_y = math.floor((-5 * y) + 5)
	print("X IDX: ", idx_x, x)
	print("Y IDX: ", idx_y, y)

	if(matrix_L[idx_x, idx_y] == numpy.float64(0.0) or matrix_R[idx_x, idx_y] == numpy.float64(0.0)):
		print("Nothing")
		pwmL = 15
		pwmR = 15
	else:
		pwmL = matrix_L[idx_x, idx_y]
		pwmR = matrix_R[idx_x, idx_y]
	
	print("LEFT: ", pwmL)
	print("RIGHT: ", pwmR)


	left_motor.ChangeDutyCycle(pwmL)

	right_motor.ChangeDutyCycle(pwmR)

	#if abs(x) < 0.1 and abs(y) < 0.1:
	#	right_motor_forward.ChangeDutyCycle(pwmy)


def control_payload(data):
	a = data['A']

	if( a == 1 ):
		command = 'H'
	else:
		command = 'L'

	#ser.write(command)

	if command == 'H':
		print('Led on')
	elif command == 'L':
		print('Led off')


def main():
	while True:
		#rand = random.randint(0, 10)
		message, address = serverSocket.recvfrom(1024)
		message = message.upper()

		try:
			time.sleep(.1)
			data = json.loads(message)
			control_motor(data)
			control_payload(data)
		except ValueError, e:
			print "Error"
		
		data = json.loads(message)
		#if rand >= 4:
		serverSocket.sendto(message,address)

	#ser.close()


if __name__=='__main__':
	main()





def f(x):
	return {
		'a':1,
		'b':2,
	}.get(x, 9) # 9 is default if x not found
