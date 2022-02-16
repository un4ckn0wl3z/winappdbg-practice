# ReWriteing from parsiya.net


import winappdbg
import argparse
import winapputil
from winappdbg.win32 import PVOID, DWORD, HANDLE
import winappdbg


class DebugEvents(winappdbg.EventHandler):
    """
    Event handler class.
    event: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/event.py
    """

    # Better hooking
    # https://winappdbg.readthedocs.io/en/latest/Debugging.html#example-9-intercepting-api-calls

    """
    LONG WINAPI RegQueryValueEx(
      _In_        HKEY    hKey,
      _In_opt_    LPCTSTR lpValueName,
      _Reserved_  LPDWORD lpReserved,
      _Out_opt_   LPDWORD lpType,
      _Out_opt_   LPBYTE  lpData,
      _Inout_opt_ LPDWORD lpcbData
    );
    """

    apiHooks = {

        # Hooks for the adviapi32.dll library
        # Can also hook kernel32.dll
        "advapi32.dll": [

            # RegQueryValueEx
            # https://msdn.microsoft.com/en-us/library/windows/desktop/ms724911(v=vs.85).aspx
            # ("RegQueryValueExW", (HANDLE, PVOID, PVOID, PVOID, PVOID, PVOID)),
            ("RegQueryValueExW", 6),

        ],
    }

    def pre_RegQueryValueExW(self, event, ra, hKey, lpValueName, lpReserved,
                             lpType, lpData, lpcbData):

        # Store the pointer for later use
        self.hKey = hKey
        self.lpValueName = lpValueName
        self.lpType = lpType
        self.lpData = lpData
        self.lpcbData = lpcbData

    def post_RegQueryValueExW(self, event, retval):
        process = event.get_process()

        process.suspend()

        table = winappdbg.Table("\t")
        table.addRow("", "")

        # Need to watch out for optional parameters
        if self.lpType is not 0:
            keyType = process.read_dword(self.lpType)
            table.addRow("keyType", keyType)

        valueName = process.peek_string(self.lpValueName, fUnicode=True)
        size = process.read_dword(self.lpcbData)

        table.addRow("valueName", valueName)
        table.addRow("size", size)

        if self.lpData is not 0:
            data = process.read(self.lpData, size)
            table.addRow("data", data)
            table.addRow("data-hex", data.encode("hex"))

        mylogger.log_text(table.getOutput())
        mylogger.log_text("-"*30)

        process.resume()


# ---------------

"""
Debug an app with parameters passed by -run
e.g. python 02-debug2.py c:\windows\system32\notepad.exe c:\textfile.txt
print system info with -i or --sysinfo
print current processes if nothing is passed
attach to a process with --attach-process or -pid
attach to a process using name with -pname or --attach-process-name
log to file with -o or --output
"""


def main():
    parser = argparse.ArgumentParser(description="WinAppDbg stuff.")
    # Make -r and -pid mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--run", nargs="+",help="path to application followed by parameters")
    group.add_argument("-pid", "--attach-pid", type=int, dest="pid",help="pid of process to attach and instrument")
    group.add_argument("-pname", "--attach-process-name", dest="pname",help="pid of process to attach and instrument")

    parser.add_argument("-i", "--sysinfo", action="store_true",help="print system information")

    # Add optional log file
    parser.add_argument("-o", "--output", dest="output", help="log filename")

    args = parser.parse_args()

    # Setup logging
    # https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/textio.py#L1766

    global mylogger
    if args.output:
        # verbose=False disables printing to stdout
        mylogger = winappdbg.Logger(args.output, verbose=False)
    else:
        mylogger = winappdbg.Logger()

    # Create an instance of our eventhandler class
    myeventhandler = DebugEvents()

    if (args.run):
        try:
            myutil = winapputil.WinAppUtil(cmd=args.run,
                                           eventhandler=myeventhandler,
                                           logger=mylogger)

            debug = myutil.debug()
            debug.loop()

        except winapputil.DebugError as error:
            mylogger.log_text("Exception in %s: %s" %
                              (error.pid_pname, error.msg))

        except KeyboardInterrupt:

            debug.stop()
            mylogger.log_text("Killed process")

    elif args.pid:
        try:
            myutil = winapputil.WinAppUtil(pid_pname=args.pid, logger=mylogger,
                                           eventhandler=myeventhandler,
                                           attach=True)
            debug = myutil.debug()
            debug.loop()

        except winapputil.DebugError as error:
            mylogger.log_text("Exception in %s: %s" % (error.pid_pname,
                                                       error.msg))

        except KeyboardInterrupt:

            debug.stop()
            mylogger.log_text("Killed process")

    elif args.pname:
        try:
            myutil = winapputil.WinAppUtil(pid_pname=args.pname,
                                           logger=mylogger,
                                           eventhandler=myeventhandler,
                                           attach=True)
            debug = myutil.debug()
            debug.loop()

        except winapputil.DebugError as error:
            mylogger.log_text("Exception in %s: %s" % (error.pid_pname,
                                                       error.msg))

        except KeyboardInterrupt:

            debug.stop()
            mylogger.log_text("Killed process")

    elif args.sysinfo:
        myutil = winapputil.WinAppUtil()
        print (myutil.sysinfo())

    else:
        myutil = winapputil.WinAppUtil()
        print (myutil.get_processes())

    pass


if __name__ == "__main__":
    main()