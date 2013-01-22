from ConfigParser import SafeConfigParser

class ParseConfig():
    def __init__(self):
        self.parser = SafeConfigParser()
        self.inet_dev = ''
        self.convert = ''
        self.username = ''
        self.password = ''
        self.smtp_srv = ''
        self.port = ''
        self.to = ''
        self.subject = ''
        
        #read config file
        self.parser.read('config.ini')

    def getmiscvar(self):
        self.inet_dev = self.parser.get('misc', 'inet_dev')
        self.convert = self.parser.get('misc', 'convert')
        return self.inet_dev, self.convert
    
    def getmailvar(self):
        self.username = self.parser.get('mail_options', 'username')
        self.password = self.parser.get('mail_options', 'password')
        self.smtp_srv = self.parser.get('mail_options', 'smtp_srv')
        self.port = self.parser.get('mail_options', 'port')
        self.to = self.parser.get('mail_options', 'to')
        self.subject = self.parser.get('mail_options', 'subject')
        return self.username, self.password, self.smtp_srv, self.port, self.to, self.subject
