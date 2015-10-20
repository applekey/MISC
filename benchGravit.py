import os

def runCommands(commands):
    for command in commands:
        print command
        #os.system(command)


##main
calls = []
gravitLocation = '~/documents/gravit/build/bin/'
objLocation = '~/documents/obj/'
outputLocation = '~/documents/obj/monkey'

## render 1

args = '3 10 10 -10 1.6 512'
call1 = gravitLocation + './gvtFileLoad' + ' '+objLocation + 'monkeyLarge.obj' + ' '+args +' '+ outputLocation
calls.append(call1)


runCommands(calls)
