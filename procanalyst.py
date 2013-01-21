#!/usr/bin/env python

import os
import sys
import web
import psutil
from convert import HumanReadable
from configparse import ParseConfig
urls = (
        '/', 'Index',
        '/proc', 'ProcList',
        '/favicon.ico', 'favicon',
        )
class favicon(object):
    """
    On base web.py process, the request for favicon.ico 404s, this make it
    displayable and thus avoid the 404s.
    """
    def GET(self):
        raise web.redirect('static/favicon.ico')

class ProcList(object):
    """
    Class to render the ProcList a.k.a /proc, which displays list of processes.
    """
    def GET(self):
        # https://groups.google.com/forum/?fromgroups=#!topic/webpy/QWOJBZMyhI4
        render = web.template.render('templates/')
        proclist = psutil.get_process_list()
        return render.proclist(proclist)

class Index(object):
    """
    Class to render the index a.k.a / path of the web server
    """
    def __init__(self):
        self.inet_dev, self.convert, self.username, self.password, self.smtp_srv = ParseConfig().getvals()
        
    def GET(self):
        render = web.template.render('templates/')
        device = self.inet_dev # change this to reflect your network device
        cpus = psutil.NUM_CPUS
        if self.convert:
            up = HumanReadable(psutil.network_io_counters(pernic=True)[device].bytes_sent).bytes2human()
            down = HumanReadable(psutil.network_io_counters(pernic=True)[device].bytes_recv).bytes2human()
            phymem = HumanReadable(psutil.TOTAL_PHYMEM).bytes2human()
        else:
            up = psutil.network_io_counters(pernic=True)[device].bytes_sent
            down = psutil.network_io_counters(pernic=True)[device].bytes_recv
            phymem = psutil.TOTAL_PHYMEM

        disks_name = self.get_disk_usage().keys()
        disks = self.get_disk_usage()
        return render.index(up, down, cpus, phymem, disks, disks_name)
    

    def get_disk_usage(self):
        disk_usages = {}
        for i in psutil.disk_partitions():
            usage = psutil.disk_usage(i.mountpoint)
            if self.convert:
                usage_total = HumanReadable(usage.total).bytes2human()
                usage_used = HumanReadable(usage.used).bytes2human()
            else:
                usage_total = usage.total
                usage_used = usage.used
            disk_usages[i.mountpoint] = {'total':usage_total,'used':usage_used,'fstype':i.fstype}
        return disk_usages


if not os.getuid() == 0:
    sys.exit('\n[WARNING!] This needs to run as root/administrator! [WARNING!]\n')
else:
    if __name__ == "__main__":
        app = web.application(urls, globals())
        app.run()
