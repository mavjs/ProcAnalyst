#!/usr/bin/env python

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
            if proc.pid == 0:
                pass
            else:
                f.write("%s,%s,%s,%s,%s" % (proc.id, proc.name, proc.username, proc.exe, proc.status))
        f.close()

    def sendcsv(self):
        send = AdminSend(self.csvname)
        send.send()


def main():
    app = ProcCSV()
    app.writecsv()
    app.sendcsv()

if __name__ == "__main__":
    main()
