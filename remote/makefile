.PHONY: install clean

install: listenerSB.py
	cp startCRATER /etc/init.d/
	update-rc.d startCRATER defaults
	cp listenerSB.py /usr/sbin/listenerSB.py
	chmod +x /usr/sbin/listenerSB.py

uninstall:
	-rm /usr/sbin/listenerSB.py
	-update-rc.d startCRATER remove
	-rm /etc/init.d/startCRATER