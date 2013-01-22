import smtplib
import mimetypes
import email
import email.mime.application
from configparse import ParseConfig

class AdminSend():
    def __init__(self, attach):
        self.attachement = attach
        self.email, self.password, self.smtp_srv, self.port, self.to, \
                self.subject = ParseConfig().getmailvar()

    def send(self):
        msg = email.mime.Multipart.MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.email
        msg['To'] = self.to

        #email body
        body = email.mime.Text.MIMEText('''This is the current process monitor
        from ProcAnalyst''')
        msg.attach(body)

        #email attachement
        fp = open(self.attchment, 'rb')
        att = email.mime.application.MIMEApplication(fp.read(),_subtype="csv")
        fp.close()
        att.add_header('Content-Disposition', 'attachment',filename=self.attachment)
        msg.attach(att)

        #send through smtp
        s = smtplib.SMTP_SSL(self.smtp_srv, self.port)
        s.starttls()
        s.login(self.email, self.password)
        s.sendmail(self.email,[self.to], msg.as_string())
        s.quit()
