#!/bin/bash

REQS="
^python[0-9]*$
^python-pyqt5$
^google-chrome.*$
^ffmpeg$
^yt-dlp$
^mpv$
"

calc_ID () {
    SHA="$(pwd | tr -d '\n' | sha256sum | cut -c 1-32)"
    for (( i=0; i < ${#SHA}; i++ )); do
        printf "\x$(printf %x $(printf %d $(( 16#${SHA:$i:1} + 97 ))))"
    done
}

ID="$(calc_ID)"
USER="$(whoami)"
LOADER="com.mpvnet.loader"
LOADER_PATH="/home/${USER}/.config/google-chrome/NativeMessagingHosts/"

echo "[*] Checking for requirements..."
for REQ in $REQS; do
    REQ_GREP="$(pacman -Qq | grep $REQ)"
    if [ "$REQ_GREP" == "" ]; then
        echo -e "\nNo package matching regex: \"$REQ\", exiting..."
        exit 1
    fi
done

echo "[*] Installing loader..."
mkdir -p $LOADER_PATH
cat ${LOADER}.json \
    | sed -e "s/#USER/${USER}/g; s/#ID/${ID}/g;" \
    > ${LOADER_PATH}${LOADER}.json
cp ${LOADER}.py $LOADER_PATH
chmod +x ${LOADER_PATH}${LOADER}.py

echo -e "\nDone!"
echo -e "In Chrome navigate to 'Extensions' > 'Manage Extensions'."
echo -e "Enable 'Developer Mode' and click 'Load Unpacked'."
echo -e "Select mpvnet directory to complete the installation."
exit 0
