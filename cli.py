#!/usr/bin/env python3

import cmd
import subprocess
import yaml

class TestCmd(cmd.Cmd):
    prompt = "schism> "

    def __init__(self):
        super().__init__()
        self.yaml = []

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
        #arg = args.split()[0];
        with open('links/current.yml', 'r') as f:
            self.yaml = yaml.load(f, Loader=yaml.FullLoader)
            print(repr(self.yaml))

    def do_done(self,args):
        if "Undone" in self.yaml.keys() and "Done" in self.yaml.keys():
            print(args)
            key = args.split()[0].lower().title()
            pos = int(args.split()[1])
            command = CommandArgValidator("done", args)
            print("The command is valid: " , command.is_valid())
            print("Command error message: " , command.message)
            try:
                task = self.yaml['Undone'][key].pop(pos)
                self.yaml['Done'][key].append(task)
            except IndexError:
                print ("Undone list",key," does not contain ", pos + 1 , "items")
            print(repr(self.yaml))

        else:
            print(self.yaml.keys())

    def do_write(self, args):
        with open('links/current.yml', 'w') as f:
            yaml.dump(self.yaml, f, Dumper=yaml.Dumper)
            print(repr(self.yaml))

    def do_play(self, args):
        process=subprocess.run(['play', '~/Music/Bash/relax.mp3'], universal_newlines=True)

if __name__ == '__main__':
    cli = TestCmd()
    cli.cmdloop()
