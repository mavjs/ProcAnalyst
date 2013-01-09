#!/usr/bin/env python
import web
import psutil

urls = (
        '/', 'Index',
        '/proc', 'ProcList',
        '/favicon.ico', 'favicon',
        )
class favicon(object):
    def GET(self):
        raise web.redirect('static/favicon.ico')

class ProcList(object):
    def GET(self):
        # https://groups.google.com/forum/?fromgroups=#!topic/webpy/QWOJBZMyhI4
        render = web.template.render('templates/')
        proclist = psutil.get_process_list()
        return render.proclist(proclist)

class Index(object):
    def GET(self):
        render = web.template.render('templates/')
        device = ['p1p1'] # change this to reflect your network device
        up = self.bytes2human(psutil.network_io_counters(pernic=True)[device[0]].bytes_sent)
        down = self.bytes2human(psutil.network_io_counters(pernic=True)[device[0]].bytes_recv)
        cpus = psutil.NUM_CPUS
        phymem = self.bytes2human(psutil.TOTAL_PHYMEM)
        disks_name = self.get_disk_usage().keys()
        disks = self.get_disk_usage()
        return render.index(up, down, cpus, phymem, disks, disks_name)
    
    def bytes2human(self,n):
        # taken from https://psutil.googlecode.com/svn/trunk/examples/disk_usage.py
        # http://code.activestate.com/recipes/578019
        # >>> bytes2human(10000)
        # '9.8K'
        # >>> bytes2human(100001221)
        # '95.4M'
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i+1)*10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n

    def get_disk_usage(self):
        disk_usages = {}
        for i in psutil.disk_partitions():
            usage = psutil.disk_usage(i.mountpoint)
            usage_total = self.bytes2human(usage.total)
            usage_used = self.bytes2human(usage.used)
            disk_usages[i.mountpoint] = {'total':usage_total,'used':usage_used,'fstype':i.fstype}
        return disk_usages


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
