all:

install:
	@echo -e "\n[*] Installing loader...\n"
	mkdir -p ${LOADER_PATH}
	cat ${LOADER}.json | sed -e "s/#USER/${USER}/g;" > ${LOADER_PATH}${LOADER}.json
	cp ${LOADER}.py ${LOADER_PATH}
	chmod +x ${LOADER_PATH}${LOADER}.py
	@echo -e "\n[*] Building extension...\n"
	${ZIP} -qr ${EXTENSION} img manifest.json popup.{html,css,js}
	@echo -e  "\n[*] Installing extension..."
	${FIREFOX} ${EXTENSION}
	@echo -e "\nDone!"
	@echo -e "A Firefox popup window should be opened by now."
	@echo -e "Click \"Add\" to complete the installation.\n"

clean:
	rm -rf autom4te.cache
	rm -rf aclocal.m4
	rm -rf config.{log,status}
	rm -rf configure
	rm -rf install-sh
	rm -rf missing
	rm -rf Makefile{.in,}
	rm -rf ${EXTENSION}