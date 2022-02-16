from winappdbg import Debug

program = ['C:\\windows\\syswow64\\notepad.exe']
debug = Debug()
proc = debug.execv(program)

debug.loop()