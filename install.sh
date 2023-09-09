#!/bin/bash

REQS="
^python[0-9]*$
^python-pyqt5$
^firefox.*$
^ffmpeg$
^yt-dlp$
^mpv$
^zip$
"

USER="$(whoami)"
LOADER="com.mpvnet.loader"
LOADER_PATH="/home/${USER}/.mozilla/native-messaging-hosts/"
EXTENSION="mpvnet.xpi"
FF_BIN="firefox"

echo "[*] Checking for requirements..."
for REQ in $REQS; do
    REQ_GREP="$(pacman -Qq | grep $REQ)"
    if [ "$REQ_GREP" == "" ]; then
        echo -e "\nNo package matching regex: \"$REQ\", exiting..."
        exit 1
    fi
    if echo "$REQ_GREP" | grep -q "firefox"; then
        FF_BIN="$REQ_GREP"
    fi
done

echo "[*] Installing loader..."
mkdir -p $LOADER_PATH
cat ${LOADER}.json \
    | sed -e "s/#USER/${USER}/g;" \
    > ${LOADER_PATH}${LOADER}.json
cp ${LOADER}.py $LOADER_PATH
chmod +x ${LOADER_PATH}${LOADER}.py

echo "[*] Building extension..."
zip -qr $EXTENSION \
    img \
    manifest.json \
    popup.{html,css,js} \

echo "[*] Installing extension..."
$FF_BIN $EXTENSION

echo -e "\nDone!"
echo -e "A Firefox popup window should be opened by now."
echo -e "Click \"Add\" to complete the installation."
exit 0
