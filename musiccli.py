#!/usr/bin/env python3

import cmd
import subprocess
import yaml
import os
import time
from random import shuffle

DANGER = "\033[31m"     #red
CAUTION = "\033[33m"    #yellow
INFO = "\033[36m"       #cyan
GOOD = "\033[32m"       #green
ERROR = "\033[34m"      #blue
WARNING = "\033[35m"    #purple
END = "\033[0m"         #white

class TestCmd(cmd.Cmd):
    prompt = GOOD + " music> " + END

    def __init__(self):
        super().__init__()
        self.play_process = None
        self.playlist_yml = ""

    def precmd(self, line):
        taskcli_history=os.path.expanduser('~/.schism/history/music_history')
        timestamp=str(int(time.time()))
        with open(taskcli_history, 'a') as f:
            f.write(line + '\n')
            f.write('#' + timestamp + '\n')
        return line

    def record_song(self,song):
        song_history=os.path.expanduser('~/.schism/history/song_history')
        timestamp=str(int(time.time()))
        with open(song_history, 'a') as f:
            f.write(song + '\n')
            f.write('#' + timestamp + '\n')

    def play_song(self,directory, song, message=""):
        self.record_song(song)
        self.play_process = subprocess.Popen(['play', directory + song], stderr=subprocess.DEVNULL)
        print(message)
        self.play_process.wait()

    def do_play(self, args):
        music_dir = os.path.expanduser('~/.schism/play/')
        subprocess.Popen(['play', music_dir + "BlasterMaster7.ogg"], stderr=subprocess.DEVNULL)

    def do_ls(self,args):
        yml_dir = os.path.expanduser('~/.schism/play/playlists/')
        for entry in os.scandir(yml_dir):
            print(entry.name)


    def do_load(self,args):
        yml_dir = os.path.expanduser('~/.schism/play/playlists/')
        arg = args.split()
        try:
            with open(yml_dir + arg[0], 'r') as f:
                text=f.read()

            self.playlist_yml=yaml.load(text, Loader=yaml.Loader)

        except FileNotFoundError:
            print("No file by name ", arg[0], " in ", yml_dir)

    def do_playlist(self,args):
        play_dir = self.playlist_yml['directory']
        message = self.playlist_yml['message']

        if self.playlist_yml['repeat'] is False:
            if self.playlist_yml['random'] is True:
                shuffle(self.playlist_yml['file'])
            for song_file in self.playlist_yml['file']:
                self.play_song(play_dir, song_file, message)
        else:
            while True: 
                if self.playlist_yml['random'] is True:
                    shuffle(self.playlist_yml['file'])
                for song_file in self.playlist_yml['file']:
                    self.play_song(play_dir, song_file, message)
                    
    def do_quit(self,args):
        return True

    def do_exit(self,args):
        return True

if __name__ == '__main__':
    cli=TestCmd()
    cli.cmdloop()
