#!/usr/bin/env python3

import cmd
import subprocess
import yaml

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

    def do_load(self, args):
        arg_list = args.split();
        with open('links/current.yml') as f:
            yml = yaml.load(f, Loader=yaml.FullLoader)
            print(arg_list)
            print(repr(yml))
            for item in yml:
                if arg_list[0] in item.keys():
                    print(arg_list[0])
                else:
                    print("Not: " + arg_list[0])

if __name__ == '__main__':
    cli = TestCmd()
    cli.cmdloop()
