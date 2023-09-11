#!/usr/bin/env python3

import os
import sys
import struct
import yt_dlp

import subprocess as sp

from multiprocessing import Process

from PyQt5.QtCore import (
    QThread,
    pyqtSignal
)

from PyQt5.QtWidgets import(
    QLabel,
    QWidget,
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QProgressBar,
    QApplication
)

PREFER_EXT = {
    'video': 'mp4',
    'audio': 'mp3'
}

class DLoader (QWidget):
    def __init__ (self, url, ydl_opts, info):
        super().__init__()
        self.info_label = QLabel()
        self.info_label.setText(info)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.cancel_download)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.info_label)
        self.vbox.addWidget(self.progress_bar)
        self.vbox.addWidget(self.cancel_button)
        self.thread = DLoaderThread(url, ydl_opts)
        self.thread.signal_progress.connect(self.set_progress)
        self.setWindowTitle('mpvnet')
        self.setFixedSize(self.sizeHint())
        self.setLayout(self.vbox)
        self.show()

    def start_download (self):
        self.thread.start()

    def cancel_download (self):
        self.thread.interrupt = True

    def set_progress (self, progress):
        self.progress_bar.setValue(progress)

class DLoaderThread (QThread):
    signal_progress = pyqtSignal(int)
    def __init__ (self, url, ydl_opts):
        super().__init__()
        self.url = url
        self.ydl_opts = ydl_opts
        self.ydl_opts.update({
            'progress_hooks': [self.progress_hook],
        })
        self.interrupt = False

    def run (self):
        with yt_dlp.YoutubeDL(self.ydl_opts.copy()) as ydl:
            try:
                ydl.download(self.url)
            except yt_dlp.DownloadCancelled:
                pass
            finally:
                QApplication.quit()

    def progress_hook (self, stream):
        if stream['status'] == 'downloading':
            if self.interrupt:
                raise yt_dlp.DownloadCancelled
            progress = int(float(stream['_percent_str'].replace('%', '')))
            if progress >= 0 and progress <= 100:
                self.signal_progress.emit(progress)

class DLoaderPathChooser:
    def __init__ (self, default_path):
        self.path = None
        self.default_path = default_path

    def choose_path (self):
        app = QApplication([])
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.selectFile(self.default_path)
        if dialog.exec():
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
    mpv_head = f'mpv --profile=pseudo-gui --geometry=x50%'
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
            sp.Popen(f'{mpv_head} {mpv_tail}', shell=True)
        else:
            sp.Popen(f'{mpv_head} --no-video {mpv_tail}', shell=True)
    else:       
        title = media_info['title']
        for symbol in ['/', '"', '\'']:
            title = title.replace(symbol, '_')
        path_chooser = DLoaderPathChooser(title)
        path_chooser.choose_path()
        if not path_chooser.path:
            stop_loader(0, 'return_normal')
        ydl_opts.update({
            'format': loader_args[2],
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
        info_str = str(
            f'Downloading {loader_args[1]}: ' +
            f'"{path_chooser.path}.{PREFER_EXT[loader_args[1]]}"'
        )
        app = QApplication([])
        downloader = DLoader(loader_args[3], ydl_opts, info_str)
        downloader.start_download()
        app.exec()
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