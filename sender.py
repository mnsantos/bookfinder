import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


class Sender:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send(self, email, file_name):
        print "Sending email to " + email
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = email
        msg['Date'] = formatdate(localtime=True)

        with open(file_name, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(file_name)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file_name)
            msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(self.email, self.password)
         
        server.sendmail(msg['From'], email , msg.as_string())