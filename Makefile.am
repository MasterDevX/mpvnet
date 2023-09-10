all:

install:
	@echo "[*] Installing loader..."
	mkdir -p ${LOADER_PATH}
	cat ${LOADER}.json | sed -e "s/#USER/${USER}/g;" > ${LOADER_PATH}${LOADER}.json
	cp ${LOADER}.py ${LOADER_PATH}
	chmod +x ${LOADER_PATH}${LOADER}.py
	@echo "[*] Building extension..."
	${ZIP} -qr ${EXTENSION} img manifest.json popup.{html,css,js}
	@echo "[*] Installing extension..."
	${FF_BIN} ${EXTENSION}
	@echo "\nDone!"
	@echo "A Firefox popup window should be opened by now."
	@echo "Click \"Add\" to complete the installation."
