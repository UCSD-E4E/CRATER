.PHONY: install clean

install: listenerSB.py
	$(MAKE) -C ../PiBits/ServoBlaster/user/ install
	cp startCRATER /etc/init.d/
	update-rc.d startCRATER defaults
	cp listenerSB.py /usr/sbin/listenerSB.py

uninstall:
	-$(MAKE) -C ../PiBits/ServoBlaster/user/ uninstall
	-rm /usr/sbin/listenerSB.py
	-update-rc.d startCRATER remove
	-rm /etc/init.d/startCRATER