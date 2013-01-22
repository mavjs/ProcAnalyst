#!/usr/bin/env python

import os
import sys
import psutil
from emailsend import AdminSend

class ProcCSV():
    def __init__(self):
        self.csvname = 'procanalyst.csv'

    def writecsv(self):
        proclist = psutil.get_process_list()
        f = open(self.csvname,'wb+')
        f.write("ProcID, ProcName,ProcUser, ProcExe, ProcStatus")
        for proc in proclist:
            if os.name == 'nt':
                f.write("%s,%s,%s" % (proc.id, proc.name, proc.username))
            elif os.name == 'posix':
                f.write("%s,%s,%s,%s,%s" % (proc.id, proc.name, proc.username, proc.exe, proc.status))
        f.close()

    def sendcsv(self):
        send = AdminSend(self.csvname)
        send.send()


def main():
    app = ProcCSV()
    app.writecsv()
    app.sendcsv()

if os.name == 'posix':
    if not os.getuid() == 0:
        sys.exit('\n[WARNING!] This needs to run as root/administrator! [WARNING!]\n')
    else:
        if __name__ == "__main__":
            main()
elif os.name == 'nt':
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin() == 1:
        sys.exit('\n[WARNING!] This needs to run as root/administrator! [WARNING!]\n')
    else:
        if __name__ == "__main__":
            main()
