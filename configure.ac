AC_PREREQ([2.69])

AC_INIT([mpvnet], [1.0])

AM_INIT_AUTOMAKE([
	1.12
	subdir-objects
	foreign
])

AC_CONFIG_SRCDIR([configure.ac])

AC_CHECK_PROGS([PYTHON], [python])
if test "x$PYTHON" = "x"; then
    AC_MSG_ERROR([Python not found])
fi

AC_CHECK_PROGS([FFMPEG], [ffmpeg])
if test "x$FFMPEG" = "x"; then
    AC_MSG_ERROR([FFmpeg not found])
fi

AC_CHECK_PROGS([YT_DLP], [yt-dlp])
if test "x$YT_DLP" = "x"; then
    AC_MSG_ERROR([yt-dlp not found])
fi

AC_CHECK_PROGS([MPV], [mpv])
if test "x$MPV" = "x"; then
    AC_MSG_ERROR([mpv not found])
fi

AC_CHECK_PROGS([CHROME], [ \
    google-chrome-stable \
    google-chrome-unstable \
    google-chrome-beta \
])
if test "x$CHROME" = "x"; then
    AC_MSG_ERROR([Google Chrome not found])
fi

AC_MSG_CHECKING([for PyQt5 Python module])
PYQT5_FOUND="no"
if $PYTHON -c "import PyQt5"; then
    PYQT5_FOUND="yes"
fi
AC_MSG_RESULT([$PYQT5_FOUND])
if test "$PYQT5_FOUND" = "no"; then
    AC_MSG_ERROR([PyQt5 Python module not found])
fi

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

AC_SUBST([CHROME])
AC_SUBST([USER])
AC_SUBST([LOADER])
AC_SUBST([LOADER_PATH])
AC_SUBST([ID])

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
