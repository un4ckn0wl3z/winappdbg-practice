from winappdbg import *


program = ['C:\\windows\\system32\\notepad.exe']

def bp_MessageBoxW_handler(event):
    print "[+] user32!MessageBoxW Triggered!"
    thread = event.get_thread()
    process = event.get_process()
    thread_ctx = thread.get_context()
    
    print "[+] MessageBoxW hWnd [RCX]:", thread_ctx['Rcx']
    print "[+] MessageBoxW lpText [RDX]:", process.peek_string(thread_ctx['Rdx'], fUnicode=True)
    print "[+] MessageBoxW lpCaption [R8]:", process.peek_string(thread_ctx['R8'], fUnicode=True)
    print "[+] MessageBoxW uType [R9]:", thread_ctx['R9']
    
def event_handler(event):
    code = event.get_event_code()
    if code == win32.LOAD_DLL_DEBUG_EVENT:
        module = event.get_module()
        if module.match_name("user32.dll"):
            pid = event.get_pid()
            address = module.resolve("MessageBoxW")
            event.debug.break_at(pid, address,  bp_MessageBoxW_handler)
            print "[+] Setting Breakpoint at user32!MessageBoxW" 
            

debug = Debug(event_handler, bKillOnExit = True)
proc = debug.execv(program)
print "[+] Launching Process!"

debug.loop()