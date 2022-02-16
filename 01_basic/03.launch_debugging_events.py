from winappdbg import Debug


pid = 44960

def event_handler(event):
    code = event.get_event_code()
    print "Debug Event Code :", code


debug = Debug(event_handler, bKillOnExit = True)
proc = debug.attach(pid)
print "[+] Attacking to pid:", pid

debug.loop()