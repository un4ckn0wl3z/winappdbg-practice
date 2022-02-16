from winappdbg import *


program = ['C:\\windows\\system32\\notepad.exe']

def prehk_MessageBoxW_handler(event, ra, handle, lpText, lpCaption, uType):
    print "[+] user32!MessageBoxW hooked!"
    pid = event.get_pid()
    process = Process(pid)
    bits = process.get_bits()
    
    msgbox_title = process.peek_string(lpCaption, fUnicode=True)
    msgbox_body = process.peek_string(lpText, fUnicode=True)
    
    print "[+] MessageBoxW title address:", HexDump.address(lpCaption, bits)
    print "[+] MessageBoxW body address:", HexDump.address(lpText, bits)
    
    print "[+] MessageBoxW title:", msgbox_title
    print "[+] MessageBoxW body:", msgbox_body
    
    process.write(lpCaption, "X");
    
    
    
def event_handler(event):
    code = event.get_event_code()
    if code == win32.LOAD_DLL_DEBUG_EVENT:
        module = event.get_module()
        if module.match_name("user32.dll"):
            pid = event.get_pid()
            msgbox_address = module.resolve("MessageBoxW")
            print "[+] Setting Hook at user32!MessageBoxW"
            
            '''
            int MessageBoxW(
                [in, optional] HWND    hWnd,
                [in, optional] LPCWSTR lpText,
                [in, optional] LPCWSTR lpCaption,
                [in]           UINT    uType
            );
            '''
            sig_msgbox = (win32.HANDLE, win32.PVOID, win32.PVOID, win32.UINT)
            event.debug.hook_function(pid, msgbox_address, preCB=prehk_MessageBoxW_handler, signature=sig_msgbox)
            
debug = Debug(event_handler, bKillOnExit=True)
proc = debug.execv(program)
print "[+] Launching Process!"

debug.loop()