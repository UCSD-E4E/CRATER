Required libraries:

	python's pygame (for joystick controller)

joystick_UDP.py is the script that handles reading controls pressed on 
the controller and sending that signal through UDP as a JSON object.

testUDP.py is a simple script testbench to make the system oscillate in
a 0.5Hz sine.

Remote PI IP address is 192.168.2.104, user = pi, pw = raspberry


Steps to get everything running:
CLIENT:
run command: sudo ifconfig eth0 192.168.2.10 netmask 255.255.255.0
broadcast 192.168.2.255

run python script: python /CRATER/client/joystick_UDP.py

To pull up the camera stream:
Open up a browser and go to address:
192.168.2.104:8080/stream

I added a bash script to run these three things in order
to run type in: bash /home/connie/start.sh

REMOTE:
Everything should be started on boot:

service CRATER should be running

CRATER starts the python script CRATER/remote/listenerSB.py
and servoblaster which is in PiBits/ServoBlaster/user/servod

If you make changes to the scripts, run 
CRATER/remote/install.sh and restart the CRATER service using

sudo service CRATER stop
sudo service CRATER start
