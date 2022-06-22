#!/usr/bin/env python3

import cmd
import subprocess

class TestCmd(cmd.Cmd):
    prompt = "test> "

    def __init__(self):
        super().__init__()

    def do_print(self, args):
        print(args)

    def do_quit(self,args):
        return True

    def do_bash(self, args):
        arg_list = args.split(" ")
        print(arg_list)
        process = subprocess.run(arg_list, universal_newlines=True, stdout=subprocess.PIPE)
        print(process.stdout)
        #process = subprocess.run(args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(process.stdout)
        #print(process.stderr)

if __name__ == '__main__':
    cli = TestCmd()
    cli.cmdloop()
