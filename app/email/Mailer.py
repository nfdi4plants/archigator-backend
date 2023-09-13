import base64
import smtplib, ssl, email, time
from email.mime.image import MIMEImage
from pathlib import Path
import pystache
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.utils import make_msgid


class Mailer:
    def __init__(self, smtp_server="smtp.office365.com", port=587, username=None, password=None, sender=None,
                 receiver=None):
        self.smtp_server = smtp_server
        self.smtp_server = os.environ.get("EMAIL_SERVER", None)
        self.port = port
        self.username = username
        self.password = password
        self.sender = sender
        self.receiver = receiver

        self.root_message = MIMEMultipart('related')

        print(self.port)
        print(self.username)
        print(self.receiver)


    def create_basemail(self):
        self.root_message = MIMEMultipart('related')
        self.root_message['Subject'] = 'ARC Release'
        self.root_message["From"] = self.sender
        self.root_message["To"] = ', '.join(self.receiver)
        self.root_message['Date'] = email.utils.formatdate(localtime=True)
        self.root_message['Message-ID'] = email.utils.make_msgid()

        self.root_message.preamble = 'This is a multi-part message in MIME format.'


    def create_testmail(self, author):

        test_template = Path("app/email/templates/testmail.html").read_text()
        # test_template = open("templates/testmail.html", "r").read()

        self.create_basemail()

        msg_alternative = MIMEMultipart('alternative')
        self.root_message.attach(msg_alternative)

        template_params = {"Author": author}

        final_email_html = pystache.render(test_template, template_params)

        # message_bytes = final_email_html.encode('utf-8')
        # base64_bytes = base64.b64encode(message_bytes)
        # base64_message = base64_bytes.decode('utf-8')

        message_text = MIMEText('This is the alternative plain text message.')
        msg_alternative.attach(message_text)

        html_message = MIMEText(final_email_html, "html", _charset='UTF-8')
        # html_message = MIMEText(final_email_html, "html")
        msg_alternative.attach(html_message)


    def create_publishmail(self, author, project_name, order_url):

        test_template = Path("app/email/templates/publishmail.html").read_text()

        self.create_basemail()

        msg_alternative = MIMEMultipart('alternative')
        self.root_message.attach(msg_alternative)

        template_params = {"Author": author, "Project_name": project_name, "order_url": order_url}

        final_email_html = pystache.render(test_template, template_params)

        message_text = MIMEText('This is the alternative plain text message.')
        msg_alternative.attach(message_text)

        html_message = MIMEText(final_email_html, "html", _charset='UTF-8')
        msg_alternative.attach(html_message)


    def send_mail(self):

        context = ssl.create_default_context()

        server = smtplib.SMTP(self.smtp_server, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.sender, self.receiver, self.root_message.as_string())
        server.quit()
