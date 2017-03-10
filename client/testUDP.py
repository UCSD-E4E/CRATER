#!/usr/bin/env python
from socket import *

import sys, tty, termios
import json
from time import sleep
import numpy as np

def main():
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	clientSocket.settimeout(1)
	t = 0
	while True:
		x = np.sin(np.pi * t);
		y = np.cos(np.pi * t);
		vectorDict = {'x': x, 'y': y, 'a' : 0}
		msg = json.dumps(vectorDict)
		addr = ("192.168.2.104", 12000)
		clientSocket.sendto(msg, addr)
		t = t + 0.1
		sleep(0.1)


if __name__ == '__main__':
	main()