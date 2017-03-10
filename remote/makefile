.PHONY: install clean

install: listenerSB.py init-script
	cp init-script /etc/init.d/CRATER
	chmod +x /etc/init.d/CRATER
	update-rc.d CRATER defaults
	cp listenerSB.py /usr/sbin/CRATER
	chmod +x /usr/sbin/CRATER

uninstall:
	-rm /usr/sbin/CRATER
	-update-rc.d CRATER remove
	-rm /etc/init.d/CRATER