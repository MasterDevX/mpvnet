#!/usr/bin/env python3

import os
import sys
import dbus
import struct
import yt_dlp

import subprocess as sp

from multiprocessing import Process
from PyQt5.QtWidgets import QApplication, QFileDialog

PREFER_EXT = {
    'video': 'mp4',
    'audio': 'mp3'
}

class DLoadTracker:
    def __init__ (self):
        self.bus = dbus.SessionBus()
        self.interface = 'org.kde.JobViewV2'
        self.server = self.bus.get_object('org.kde.kuiserver', '/JobViewServer')
        self.path = self.server.requestView('mpvnet', 'download', 1)
        self.job = self.bus.get_object('org.kde.kuiserver', self.path)
        self.set_info('Initializing...')

    def set_progress (self, progress):
        self.job.setPercent(progress, dbus_interface=self.interface)

    def set_info (self, info):
        self.job.setInfoMessage(info, dbus_interface=self.interface)

    def terminate (self, info):
        self.job.terminate(info, dbus_interface=self.interface)

    def progress_hook (self, stream):
        if stream['status'] == 'downloading':
            progress = int(float(stream['_percent_str'].replace('%', '')))
            if progress >= 0 and progress <= 100:
                self.set_progress(progress)

class DLoadPathChooser:
    def __init__ (self, default_path):
        self.path = None
        self.default_path = default_path

    def choose_path (self):
        app = QApplication([])
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.selectFile(self.default_path)
        if dialog.exec_():
            self.path = dialog.selectedFiles()[0]

def recv_msg():
    size = sys.stdin.buffer.read(4)
    size = struct.unpack('I', size)[0]
    text = sys.stdin.buffer.read(size)
    return text.decode()[9:-2]

def send_msg(msg):
    text = b'{ "text": "' + msg.encode() + b'" }'
    size = struct.pack('I', len(text))
    sys.stdout.buffer.write(size)
    sys.stdout.buffer.write(text)
    sys.stdout.buffer.flush()

def run_loader(loader_args_raw):
    sys.stdout = open(os.devnull, 'w')
    os.environ['LD_PRELOAD'] = '/usr/lib/libvulkan.so.1'
    os.chdir(os.path.expanduser("~"))
    loader_args = loader_args_raw.split()
    mpv_tail = f'--ytdl-format=\'{loader_args[2]}\' \'{loader_args[3]}\''
    ydl_opts = {
        'quiet': True,
        'no_color': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts.copy()) as ydl:
        try:
            media_info = ydl.extract_info(loader_args[3], download=False)
        except yt_dlp.utils.DownloadError:
            stop_loader(0, 'return_error_invalid_url')
    if loader_args[0] == 'mpv':
        if loader_args[1] == 'video':
            sp.Popen(f'mpv --geometry=x50% {mpv_tail}', shell=True)
        else:
            sp.Popen(f'konsole -e "mpv --no-video {mpv_tail}"', shell=True)
    else:       
        tracker = DLoadTracker()
        title = media_info['title']
        for symbol in ['/', '"', '\'']:
            title = title.replace(symbol, '_')
        path_chooser = DLoadPathChooser(title)
        path_chooser.choose_path()
        if not path_chooser.path:
            tracker.terminate('Action cancelled')
            stop_loader(0, 'return_normal')
        ydl_opts.update({
            'format': loader_args[2],
            'progress_hooks': [tracker.progress_hook],
            'outtmpl': f'{path_chooser.path}.%(ext)s',
        })
        if loader_args[1] == 'video':
            ydl_opts.update({
                'merge_output_format': PREFER_EXT['video']
            })
        else:
            ydl_opts.update({
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': PREFER_EXT['audio'],
                }]
            })
        tracker.set_info(
            f'Downloading {loader_args[1]}: ' +
            f'"{path_chooser.path}.{PREFER_EXT[loader_args[1]]}"'
        )
        with yt_dlp.YoutubeDL(ydl_opts.copy()) as ydl:
            try:
                ydl.download(loader_args[3])
            except dbus.exceptions.DBusException:
                stop_loader(0, 'return_normal')
        tracker.terminate('Download complete')
    stop_loader(0, 'return_normal')

def stop_loader (return_code, return_msg):
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    send_msg(return_msg)
    sys.exit(return_code)


if __name__ == '__main__':
    loader_proc = Process(target=run_loader, args=(recv_msg(),))
    loader_proc.start()
    loader_proc.join()