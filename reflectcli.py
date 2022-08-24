#!/usr/bin/env python3
import cmd
import os
import yaml

DANGER = "\033[31m"     #red
CAUTION = "\033[33m"    #yellow
INFO = "\033[36m"       #cyan
GOOD = "\033[32m"       #green
ERROR = "\033[34m"      #blue
WARNING = "\033[35m"    #purple
END = "\033[0m"         #white

class ReflectionCli(cmd.Cmd):
    prompt=" think>"

    def __init__(self):
        super().__init__()
        self.yaml = {}

    def do_exit(self, args):
        return True

    def do_quit(self, args):
        return True

    def do_load(self, args):
        with open(os.path.expanduser('~/.schism/links/current-reflection.yml')) as f:
            text = f.read()
            self.yaml = yaml.load(text, Loader=yaml.Loader)

    def do_display(self, args):
        for key in self.yaml.keys():
            print(GOOD, key, END, '\t', self.yaml[key])

if __name__ == '__main__':
    cli = ReflectionCli()
    cli.cmdloop()
