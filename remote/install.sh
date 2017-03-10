#!/bin/sh

cp listenerSP.py /usr/sbin/CRATER
cp init-script /etc/init.d/CRATER
update-rc.d CRATER defaults
