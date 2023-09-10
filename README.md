## mpvnet
This is a Chrome / Firefox extension that allows you to play / download media across different websites with mpv / yt-dlp.

## Note
The project is currently on the very early stage of development and only works on distros with **KDE Plasma** desktop environment. Want this to change as soon as possible? Feel free to contribute!

## Features
The project offers the following functionality:
- Working on all linux distros
- Firefox / Google Chrome support
- Playing video / audio with mpv
- Video / audio downloading
- Setting video resolution limit
- Integration with KDE Shell
- Easy to use install system
- Support for [tons of websites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

## Installation
- Clone the repository. Replace `branch` with `firefox` or `chrome` depending on your browser.
```
git clone -b branch https://github.com/MasterDevX/mpvnet.git
```
- Install using autotools. Requires `autoconf` and `automake` to be present in the system.
```
autoreconf -i
./configure
make install
```
