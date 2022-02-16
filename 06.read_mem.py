from winappdbg import *


program = ['C:\\windows\\system32\\notepad.exe']

def bp_MessageBoxW_handler(event):
    print "[+] user32!MessageBoxW Triggered!"
    pid = event.get_pid()
    process = Process(pid)
    
    current_thread = event.get_thread()
    thread_ctx = current_thread.get_context()
    
    rsp = thread_ctx['Rsp']
    data = process.read(rsp, 10)
    print HexDump.hexadecimal(data)
    
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