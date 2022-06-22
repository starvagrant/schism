#!/usr/bin/env python3

import cmd

class TestCmd(cmd.Cmd):
    prompt = "test> "

    def __init__(self):
        super().__init__()

    def do_print(self, args):
        print(args)

    def do_quit(self,args):
        return True

if __name__ == '__main__':
    cli = TestCmd()
    cli.cmdloop()
