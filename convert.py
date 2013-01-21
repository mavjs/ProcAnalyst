
class HumanReadable():
    def __init__(self, num):
        self.num = num

    def bytes2human(self):
        """
        converts insane bytes into proper _human_ readable units
        - taken from https://psutil.googlecode.com/svn/trunk/examples/disk_usage.py
        - http://code.activestate.com/recipes/578019
        >>> bytes2human(10000)
        '9.8K'
        >>> bytes2human(100001221)
        '95.4M'
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i+1)*10
        for s in reversed(symbols):
            if self.num >= prefix[s]:
                value = float(self.num) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % self.num

