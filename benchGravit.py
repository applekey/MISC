import os
import time


def runCommands(commands):
    for command in commands:
        runCommand(command)

def runCommand(command):
    print command
    #os.system(command)

##main
calls = []
gravitLocation = '~/documents/gravit/build/bin/'
objLocation = '~/documents/obj/'
outputLocation = '~/documents/obj/'

objModel = 'monkeyLarge.obj'


## render 1

iterations = 10
args = '3 10 10 -10 1.6 512'
call1 = gravitLocation + './gvtFileLoad' + ' '+objLocation + objModel + ' '+args +' '+ outputLocation+objModel

executionTimes = []

for i in range(iterations):
    start_time = time.time()
    runCommand(call1)
    duration = time.time() - start_time

##output ot file
fileName = outputLocation + 'runs.txt'
f = open(fileName,'a')

f.write(objMode+'\n')
for time in executionTimes:
    f.write(time+'\n')
f.close() # you can omit in most cases as the destructor will call it
