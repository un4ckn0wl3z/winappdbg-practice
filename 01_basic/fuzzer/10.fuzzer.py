from winappdbg import *
from random import randint
import thread
from time import sleep
import shutil

program = [r'C:\\windows\\system32\\notepad.exe', 'input.txt']


def event_handler(event):
    code = event.get_event_code()
    if code == win32.EXCEPTION_DEBUG_EVENT and event.is_last_chance():
        print "[+] Exception Occured and Handled!"
        crash = Crash(event)
        crash.fetch_extra_data(event)
        details = crash.fullReport(bShowNotes=True)
        print details
        rand_fname = str(randint(0,1000))
        shutil.copyfile('input.txt', 'crashes\\'+rand_fname+'.txt')
        f = open(rand_fname+'.log', 'wb')
        f.write(details)
        f.close()

def Mutate(base):
    my_list = list(base)
    for i in range(0,2):
        offset = randint(0, len(my_list)-1)
        my_list[offset] = str(randint(0, 9))
    
    return ''.join(my_list)


def isStillRunning(proc):
    sleep(2)
    proc.kill()
    

while True:
    f = open('bases\\sample1.txt', 'rb')
    base_content = f.read()
    f.close()
    
    mutate_content = Mutate(base_content)
    f = open('input.txt', 'wb')
    f.write(mutate_content)
    f.close()
    
    debug = Debug(event_handler, bKillOnExit=True)
    proc = debug.execv(program)
    print "[+] Launching Process!"
    thread.start_new_thread(isStillRunning, (proc,))
    debug.loop()