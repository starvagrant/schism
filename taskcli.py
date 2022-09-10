#!/usr/bin/env python3

import cmd
import subprocess
import yaml
import os
import signal
import time

DANGER = "\033[31m"     #red
CAUTION = "\033[33m"    #yellow
INFO = "\033[36m"       #cyan
GOOD = "\033[32m"       #green
ERROR = "\033[34m"      #blue
WARNING = "\033[35m"    #purple
END = "\033[0m"         #white

class TestCmd(cmd.Cmd):
    prompt = GOOD + " schism> " + END

    def __init__(self):
        super().__init__()
        self.yaml = {}
        self.play_process = None
        self.play_pid = -1

    def precmd(self, line):
        taskcli_history=os.path.expanduser('~/.schism/history/taskcli_history')
        timestamp=str(int(time.time()))
        with open(taskcli_history, 'a') as f:
            f.write(line + '\n')
            f.write('#' + timestamp + '\n')
        return line

    def yaml_not_loaded(self):
        if len(self.yaml) == 0:
            return True
        else:
            return False

    def do_print(self, args):
        print(args)

    def do_quit(self,args):
        return True

    def do_bash(self, args):
        arg_list = args.split(" ")
        print(arg_list)
        process = subprocess.run(arg_list, universal_newlines=True, stdout=subprocess.PIPE)
        print(process.stdout)

    def do_load(self, args):
        #arg = args.split()[0];
        yml_file = os.path.expanduser('~/.schism/links/current-todo.yml')
        with open(yml_file, 'r') as f:

            self.yaml = yaml.load(f, Loader=yaml.FullLoader)
            print(repr(self.yaml))

    def do_todo(self, args):
        process = subprocess.run(['play', '~/.schism/play/Victory/FF6-short.mp3'])
        self.do_display('')

    def do_done(self,args):
        if self.yaml_not_loaded():
            return

        if "Undone" in self.yaml.keys() and "Done" in self.yaml.keys():
            print(args)
            key = args.split()[0].lower().title()
            pos = int(args.split()[1])
            try:
                task = self.yaml['Undone'][key].pop(pos)
                if None in self.yaml['Done'][key]:
                    self.yaml['Done'][key].pop(0)
                self.yaml['Done'][key].append(task)
                hist_file = os.path.expanduser('~/.schism/history/taskdone_history')
                with open(hist_file, 'a') as f:
                    timestamp=str(int(time.time()))
                    f.write(task + '\n')
                    f.write('#' + timestamp + '\n')

            except IndexError:
                print ("Undone list",key," does not contain ", pos + 1 , "items")
            print(repr(self.yaml))

        else:
            print(self.yaml.keys())

    def do_write(self, args):
        yml_file = os.path.expanduser('~/.schism/links/current-todo.yml')
        with open(yml_file, 'w') as f:
            yaml.dump(self.yaml, f, Dumper=yaml.Dumper)
            print(repr(self.yaml))

    def do_play(self, args):
        """
        play <name> <times>
        Play a helpful track repeatedly.
        These Include:
        game: a mash of Nintendo era soundtracks
        venus: Gustav Holst's Venus Bringer of Peace
        wakeup: FF7, Cloud's Motorcycle Sequence
        clean: Warcraft II soundtrack, tracks 2-13
        zero: almost null mp3 (stops current track)
        """

        if self.play_process is not None:
            self.play_process.kill()
        arg = args.split(' ')

        music_dir = os.path.expanduser('~/.schism/play/')

        print(arg)
        run_list = arg[0]
        if len(arg) < 2:
            arg.append(1)
            print(arg)
        else:
            print(arg)
        for x in range(int(arg[1])):
            if arg[0] == 'relax':
                self.play_process=subprocess.Popen(['play', music_dir + 'relax.mp3'], stderr=subprocess.DEVNULL)
                print('relax!!')
            if arg[0] == 'game':
                self.play_process=subprocess.Popen(['play', music_dir + 'BlasterMaster7.ogg', music_dir + 'SuperMario3BowserBattle.mp3', music_dir + 'WilyFortress.mp3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print('Blaster SM3 Wily')
            if arg[0] == 'venus':
                self.play_process = subprocess.Popen(['play', music_dir + 'venus.mp3'], stderr=subprocess.DEVNULL)
                print('Venus')
            if arg[0] == 'wakeup':
                self.play_process = subprocess.Popen(['play', music_dir + 'wakeup.mp3'], stderr=subprocess.DEVNULL)
                print('wakuep')
            if arg[0] == 'clean':
                self.play_process=subprocess.Popen(['play', music_dir + 'WarcraftII/*.ogg'], stderr=subprocess.DEVNULL)
                print('clean')
            if arg[0] == 'zero':
                self.play_process=subprocess.Popen(['play', music_dir + 'zero.mp3'], stderr=subprocess.DEVNULL)
                print('zero')

    def do_display(self,args):
        if self.yaml_not_loaded():
            return

        for todos in self.yaml['Undone'].keys():
            print(self.yaml['Undone'][todos])
            items_left = len(self.yaml['Undone'][todos])
            for item in self.yaml['Undone'][todos]:
                if items_left > 2:
                    print(CAUTION, item, END)
                else:
                    print(INFO, item, END)

    def do_scan(self,args):
        arg = args.split(' ')
        if len(arg) < 2:
            year=2022
        for entry in os.scandir(os.path.expanduser('~/.schism/time/')):
            if entry.is_file:
                if entry.name.startswith('todo' + str(year)) and entry.name.endswith('.yml'):
                    print(entry.name)

    def do_link(self,args):
        print('link a new file here!')


if __name__ == '__main__':
    cli = TestCmd()
    cli.cmdloop()
