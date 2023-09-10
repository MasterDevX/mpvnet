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

AC_CHECK_PROGS([FIREFOX], [ \
    firefox-developer-edition \
    firefox-nightly \
    firefox-beta \
    firefox-esr \
    firefox \
])
if test "x$FIREFOX" = "x"; then
    AC_MSG_ERROR([Firefox not found])
fi

AC_CHECK_PROGS([ZIP], [zip])
if test "x$ZIP" = "x"; then
    AC_MSG_ERROR([zip not found])
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

USER="$(whoami)"
LOADER="com.mpvnet.loader"
LOADER_PATH="/home/${USER}/.mozilla/native-messanging-hosts/"
EXTENSION="mpvnet.xpi"

AC_SUBST([FIREFOX])
AC_SUBST([ZIP])
AC_SUBST([USER])
AC_SUBST([LOADER])
AC_SUBST([LOADER_PATH])
AC_SUBST([EXTENSION])

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
