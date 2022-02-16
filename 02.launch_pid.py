from winappdbg import Debug


pid = 33260
debug = Debug()
proc = debug.attach(pid)
print "attaching to pid:", pid

debug.loop()