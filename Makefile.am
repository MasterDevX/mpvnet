all:

install:
	@echo -e "\n[*] Installing loader...\n"
	mkdir -p ${LOADER_PATH}
	cat ${LOADER}.json | sed -e "s/#USER/${USER}/g; s/#ID/${ID}/g;" > ${LOADER_PATH}${LOADER}.json
	cp ${LOADER}.py ${LOADER_PATH}
	chmod +x ${LOADER_PATH}${LOADER}.py
	@echo -e "\nDone!"
	@echo -e "In Chrome navigate to 'Extensions' > 'Manage Extensions'."
	@echo -e "Enable 'Developer Mode' and click 'Load Unpacked'."
	@echo -e "Select mpvnet directory to complete the installation.\n"

clean:
	rm -rf autom4te.cache
	rm -rf aclocal.m4
	rm -rf config.{log,status}
	rm -rf configure
	rm -rf install-sh
	rm -rf missing
	rm -rf Makefile{.in,}