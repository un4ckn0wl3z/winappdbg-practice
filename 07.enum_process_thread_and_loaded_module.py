from winappdbg import *


program = ['C:\\windows\\system32\\notepad.exe']

def bp_MessageBoxW_handler(event):
    print "[+] user32!MessageBoxW Triggered!"
    pid = event.get_pid()
    process = Process(pid)
    
    for thread in process.iter_threads():
        print "\t%d" % thread.get_tid()
        print thread.get_context()
    
    bits = process.get_bits()
    
    for module in process.iter_modules():
        print "\t%s\t%s" %  (HexDump.address(module.get_base(), bits), module.get_filename() )
        
    debug.detach(pid)
    
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