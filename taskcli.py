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
    prompt = GOOD + " schism> " + END

    def __init__(self):
        super().__init__()
        self.yaml = {}
        self.yml_file = ''
        self.direntry = []

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

    def do_ls(self, args):
        yml_dir = os.path.expanduser('~/.schism/ed/todo/')
        dir_content = os.scandir(yml_dir)
        self.direntry = []
        for entry in dir_content:
            self.direntry.append(entry)

        for entry in self.direntry:
            print(entry.name)

        for entry in os.scandir(yml_dir):
            print(entry.name)

    def do_load(self, args):
        yml_dir = os.path.expanduser('~/.schism/ed/todo/')
        arg = args.split()
        try:
            self.yml_file = yml_dir + arg[0]
            with open(self.yml_file, 'r') as f:
                self.yaml = yaml.load(f, Loader=yaml.SafeLoader)
                print(repr(self.yaml))

        except FileNotFoundError:
            self.yml_file = ''
            print(arg[0] + " not found in " + yml_dir)
            print("type ls for list of files")

        except IndexError:
            print("No file specified. Use ls command to view files")

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

    def do_defer(self, args):
        if self.yaml_not_loaded():
            return

        if "Undone" in self.yaml.keys():
            print(args)
            key = args.split()[0].lower().title()
            pos = int(args.split()[1])
            try:
               task = self.yaml['Undone'][key].pop(pos)
               self.yaml['Undone'][key].append(task)
               hist_file = os.path.expanduser('~/.schism/history/taskdefer_history')
               with open(hist_file, 'a') as f:
                   timestamp=str(int(time.time()))
                   f.write(task + '\n')

            except IndexError:
                print ("Undone list",key," does not contain ", pos + 1 , "items")
            print(repr(self.yaml))

    def do_write(self, args):
        try:
            with open(self.yml_file, 'w') as f:
                yaml.dump(self.yaml, f, Dumper=yaml.Dumper)
                print(repr(self.yaml))

        except FileNotFoundError:
            print('No File is Loaded')
            print('Type ls for list of files.')

    def do_display(self,args):
        if self.yaml_not_loaded():
            return

        if args == "" or args.lower() == "undone":
            for todos in self.yaml['Undone'].keys():
                print(self.yaml['Undone'][todos])
                items_left = len(self.yaml['Undone'][todos])
                for item in self.yaml['Undone'][todos]:
                    if items_left > 2:
                        print(CAUTION, item, END)
                    else:
                        print(INFO, item, END)

        if args.lower() == "done":
            for todos in self.yaml['Done'].keys():
                print(self.yaml['Done'][todos])
                items_left = len(self.yaml['Done'][todos])
                for item in self.yaml['Done'][todos]:
                    if items_left > 2:
                        print(CAUTION, item, END)
                    else:
                        print(INFO, item, END)

        if args.lower() == "defer":
            for todos in self.yaml['Defer'].keys():
                print(self.yaml['Defer'][todos])
                items_left = len(self.yaml['Defer'][todos])
                for item in self.yaml['Defer'][todos]:
                    if items_left > 2:
                        print(CAUTION, item, END)
                    else:
                        print(INFO, item, END)

    def do_queue(self, args):
        if self.yaml_not_loaded():
            return

        for todo in self.yaml['Undone'].keys():
            try:
                print(todo, ": ", self.yaml['Undone'][todo][0])
            except IndexError:
                pass

    def do_progress(self, args):
        if self.yaml_not_loaded():
            return

        if "Undone" in self.yaml.keys():
            print(args)
            key = args.split()[0].lower().title()
            pos = int(args.split()[1])
            try:
               task = self.yaml['Undone'][key].pop(pos)
               halfway = len(self.yaml['Undone'][key]) // 2
               self.yaml['Undone'][key].insert(halfway, task)
               hist_file = os.path.expanduser('~/.schism/history/taskinprogress_history')
               with open(hist_file, 'a') as f:
                   timestamp=str(int(time.time()))
                   f.write(task + '\n')

            except IndexError:
                print ("Undone list",key," does not contain ", pos + 1 , "items")
            print(repr(self.yaml))

    def do_refresh(self, args):
        if self.yaml_not_loaded():
            return

        undone_key = args.split()[0].lower().title()
        yaml_dir = os.path.expanduser('~/.schism/ed/todo/')
        yaml_file = undone_key + ".yml"
        try:
            with open(yaml_dir + yaml_file, 'r') as f:
                text = f.read()

            task_list = yaml.load(text, Loader=yaml.Loader)

        except FileNotFoundError:
            print(yaml_dir + yaml_file + " does not exist.")
            return

        if undone_key in self.yaml['Undone'].keys():
            for task in task_list:
                if task is not in self.yaml['Undone'][undone_key]:
                    self.yaml['Undone'][undone_key].append(task)

if __name__ == '__main__':
    cli = TestCmd()
    cli.cmdloop()
