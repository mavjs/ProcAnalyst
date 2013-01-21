from ConfigParser import SafeConfigParser

class ParseConfig():
    def __init__(self):
        self.parser = SafeConfigParser()
        self.inet_dev = ''
        self.convert = ''
        self.username = ''
        self.password = ''
        self.smtp_srv = ''

    def getvals(self):
        self.parser.read('config.ini')
        self.inet_dev = self.parser.get('misc', 'inet_dev')
        self.convert = self.parser.get('misc', 'convert')
        self.username = self.parser.get('mail_options', 'username')
        self.password = self.parser.get('mail_options', 'password')
        self.smtp_srv = self.parser.get('mail_options', 'smtp_srv')
        return self.inet_dev, self.convert, self.username, self.password, self.smtp_srv
