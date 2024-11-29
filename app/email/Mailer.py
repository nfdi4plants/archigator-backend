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
    """
    The `Mailer` class provides functionality to create and send email messages using SMTP server configuration.

    .. note::
        This class requires the following modules to be imported at the top of the file:

        - `os`
        - `email`
        - `smtplib`
        - `ssl`
        - `MIMEText`
        - `MIMEMultipart`
        - `email.utils.formatdate`
        - `email.utils.make_msgid`
        - `Path` (from `pathlib`)
        - `pystache`


    **Class Initialization**
    ------------------------

    ```python
    class Mailer:
        def __init__(self, smtp_server="smtp.office365.com", port=587, username=None, password=None, sender=None,
                     receiver=None):
            '''
            Initializes a new instance of the Mailer class.

            :param smtp_server: The SMTP server address. Default is 'smtp.office365.com'.
            :param port: The port number. Default is 587.
            :param username: The username for authentication. Default is None.
            :param password: The password for authentication. Default is None.
            :param sender: The email address of the sender. Default is None.
            :param receiver: The email address(es) of the receiver(s) as a list. Default is None.
            '''
    ```

    **Methods**
    ------------

    ```python
        def create_basemail(self):
            '''
            Create a base email message.

            :return: None
            '''

        def create_testmail(self, author):
            '''
            Create a test email.

            :param author: The author of the email.
            :return: None
            '''

        def create_publishmail(self, author, project_name, order_url):
            '''
            Create a publish mail.

            :param author: The author of the project being published.
            :param project_name: The name of the project being published.
            :param order_url: The URL of the order associated with the project.
            :return: None
            '''

        def create_curator_mail(self, user, project_name, submission_url):
            '''
            Create a curator mail.

            :param user: The user submitting the project for curation.
            :param project_name: The name of the project being submitted.
            :param submission_url: The URL of the submission.
            :return: None
            '''

        def send_mail(self):
            '''
            Sends an email using the given SMTP server configuration.

            :return: None
            '''
    ```

    **Attributes**
    ---------------

    ```python
            self.smtp_server = smtp_server
            self.smtp_server = os.environ.get("EMAIL_SERVER", None)
            self.port = port
            self.username = username
            self.password = password
            self.sender = sender
            self.receiver = receiver

            self.root_message = MIMEMultipart('related')
    ```
    """
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

    def create_basemail(self):
        """
        Create a base email message.

        :return: None
        """

        self.root_message = MIMEMultipart('related')
        self.root_message['Subject'] = 'ARC Release'
        self.root_message["From"] = self.sender
        self.root_message["To"] = ', '.join(self.receiver)
        self.root_message['Date'] = email.utils.formatdate(localtime=True)
        self.root_message['Message-ID'] = email.utils.make_msgid()

        self.root_message.preamble = 'This is a multi-part message in MIME format.'


    def create_testmail(self, author):
        """
        Create a test email.

        :param author: The author of the email.
        :return: None
        """

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
        """
        :param author: The author of the project being published.
        :param project_name: The name of the project being published.
        :param order_url: The URL of the order associated with the project.
        :return: None

        This method is used to create a publish mail. It takes the author, project_name, and order_url as parameters and
        does the following steps:
        1. Reads the HTML template file from the specified path.
        2. Calls the create_basemail() method.
        3. Creates a MIMEMultipart object for alternative message content.
        4. Attaches the alternative plain text message to the MIMEMultipart object.
        5. Renders the HTML template using the provided template parameters.
        6. Creates a MIMEText object for the HTML message content.
        7. Attaches the HTML message to the MIMEMultipart object.
        """
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


    def create_curator_mail(self, user, project_name, submission_url):

        curator_template = Path("app/email/templates/curator_submission.html").read_text()

        self.create_basemail()

        self.root_message['Subject'] = 'New ARC Submission is available'


        msg_alternative = MIMEMultipart('alternative')
        self.root_message.attach(msg_alternative)

        template_params = {"User": user, "Project_name": project_name, "submission_url": submission_url}

        final_email_html = pystache.render(curator_template, template_params)

        message_text = MIMEText('This is the alternative plain text message.')
        msg_alternative.attach(message_text)

        html_message = MIMEText(final_email_html, "html", _charset='UTF-8')
        msg_alternative.attach(html_message)


    def send_mail(self):
        """
        Sends an email using the given SMTP server configuration.

        :return: None
        """
        context = ssl.create_default_context()

        server = smtplib.SMTP(self.smtp_server, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.sender, self.receiver, self.root_message.as_string())
        server.quit()
