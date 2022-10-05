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

    def do_quit(self,args):
        return True

    def do_exit(self,args):
        return True

if __name__ == '__main__':
    cli=TestCmd()
    cli.cmdloop()
