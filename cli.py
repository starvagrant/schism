#!/usr/bin/env python3

import cmd
import subprocess
import yaml

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
                if None in self.yaml['Done'][key]:
                    self.yaml['Done'][key].pop(0)
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
        arg = args.split(' ')
        print(arg)
        run_list = arg[0]
        if len(arg) < 2:
            arg.append(0)
            print(arg)
        else:
            print(arg)
        if int(arg[1]) == 0:
            while True:
                song = '~/Music/Bash/' + arg[0] + '.mp3'
                process=subprocess.run(['play', song])

        for x in range(int(arg[1])):
            if arg[0] == 'relax':
                process=subprocess.run(['play', '~/Music/Bash/relax.mp3'], universal_newlines=True)
                print('relax!!')
            if arg[0] == 'game':
                process=subprocess.run(['play', '~/Music/Bash/BlasterMaster7.ogg', '~/Music/Bash/SuperMario3BowserBattle.mp3', '~/Music/Bash/WilyFortress.mp3'])
                print('Blaster SM3 Wily')
            if arg[0] == 'venus':
                process=subprocess.run(['play', '~/Music/Bash/venus.mp3'])
                print('Venus')
            if arg[0] == 'wakeup':
                process=subprocess.run(['play', '~/Music/Bash/wakeup.mp3'])
                print('wakuep')

    def do_display(self,args):
        for todos in self.yaml['Undone'].keys():
            print(self.yaml['Undone'][todos])
            items_left = len(self.yaml['Undone'][todos])
            for item in self.yaml['Undone'][todos]:
                if items_left > 2:
                    print(CAUTION, item, END)
                else:
                    print(INFO, item, END)

if __name__ == '__main__':
    cli = TestCmd()
    cli.cmdloop()
