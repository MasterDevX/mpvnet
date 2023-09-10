AC_INIT([mpvnet], [0.1])

AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE([
	1.12
	subdir-objects
	foreign
])


AC_CONFIG_SRCDIR([configure.ac])

AC_CHECK_PROG(PYTHON, python, [python])
if test "x$PYTHON" = x; then
    AC_MSG_ERROR([Python not found])
fi

AC_CHECK_PROG(FFMPEG, ffmpeg, [ffmpeg])
if test "x$FFMPEG" = x; then
    AC_MSG_ERROR([FFmpeg not found])
fi

AC_CHECK_PROG(YT_DLP, yt-dlp, [yt-dlp])
if test "x$YT_DLP" = x; then
    AC_MSG_ERROR([yt-dlp not found])
fi

AC_CHECK_PROG(MPV, mpv, [mpv])
if test "x$MPV" = x; then
    AC_MSG_ERROR([mpv not found])
fi

AC_CHECK_PROG(FF_BIN, firefox, [firefox])
if test "x$FF_BIN" = x; then
    AC_MSG_ERROR([firefox not found])
fi

AC_CHECK_PROG(ZIP, zip, [zip])
if test "x$ZIP" = x; then
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

AC_SUBST([FF_BIN])
AC_SUBST([USER])
AC_SUBST([LOADER])
AC_SUBST([LOADER_PATH])
AC_SUBST([EXTENSION])

AC_PREREQ([2.69])

AC_CONFIG_FILES([Makefile])

AC_OUTPUT
