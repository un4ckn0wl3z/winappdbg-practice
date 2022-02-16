from winappdbg import *


program = ['D:\Projects\winappdbg-practice\CrashMe.exe']


def event_handler(event):
    code = event.get_event_code()
    if code == win32.EXCEPTION_DEBUG_EVENT:
        print "[+] Exception Occured and Handled!"
        crash = Crash(event)
        crash.fetch_extra_data(event)
        details = crash.fullReport(bShowNotes=True)
        print details



debug = Debug(event_handler, bKillOnExit=True)
proc = debug.execv(program)
print "[+] Launching Process!"

debug.loop()