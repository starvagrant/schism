#!/usr/bin/env python3

import cmd
import subprocess
import yaml
import os
import time

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

    def do_play(self, args):
        music_dir = os.path.expanduser('~/.schism/play/')
        print(os.path.expanduser)
        subprocess.Popen(['play', music_dir + "BlasterMaster7.ogg"], stderr=subprocess.PIPE)

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

            self.playlist_yml=yaml.load(text, Loader=yaml.BaseLoader)

        except FileNotFoundError:
            print("No file by name ", arg[0], " in ", yml_dir)

    def do_playlist(self,args):
        print(self.playlist_yml)
        play_dir = self.playlist_yml['directory']
        for song_file in self.playlist_yml['file']:
            self.play_process = subprocess.Popen(['play', play_dir + song_file], stderr=subprocess.PIPE)
            print(self.playlist_yml['message'])
            self.play_process.wait()

    def do_quit(self,args):
        return True

    def do_exit(self,args):
        return True

if __name__ == '__main__':
    cli=TestCmd()
    cli.cmdloop()
