import os
from app.gitlab.api import Gitlab_API

from app.email.Mailer import Mailer


def send_testmail(receiver: str):
    smtp_server = os.getenv("EMAIL_SERVER")
    username = os.getenv("EMAIL_USERNAME")
    sender = os.getenv("EMAIL_SENDER")
    port = os.getenv("EMAIL_PORT")
    password = os.getenv("EMAIL_PASSWORD")

    mailer = Mailer(username=username, port=port, password=password,
                    smtp_server=smtp_server, sender=sender, receiver=receiver)

    mailer.create_testmail("Testuser")
    mailer.send_mail()


def send_mail(receiver: list, author: str, project_name: str, order_url: str):

    smtp_server = os.getenv("EMAIL_SERVER")
    username = os.getenv("EMAIL_USERNAME")
    sender = os.getenv("EMAIL_SENDER")
    port = os.getenv("EMAIL_PORT")
    password = os.getenv("EMAIL_PASSWORD")

    mailer = Mailer(username=username, port=port, password=password,
                    smtp_server=smtp_server, sender=sender, receiver=receiver)

    mailer.create_publishmail(author=author, project_name=project_name, order_url=order_url)
    print("\n\n\n sending mail \n\n\n")
    mailer.send_mail()


def send_curator_mail(receiver: list, user: str, project_name: str, submission_url: str):

    smtp_server = os.getenv("EMAIL_SERVER")
    username = os.getenv("EMAIL_USERNAME")
    sender = os.getenv("EMAIL_SENDER")
    port = os.getenv("EMAIL_PORT")
    password = os.getenv("EMAIL_PASSWORD")

    mailer = Mailer(username=username, port=port, password=password,
                    smtp_server=smtp_server, sender=sender, receiver=receiver)

    mailer.create_curator_mail(user=user, project_name=project_name, submission_url=submission_url)
    print("\n\n\n sending mail \n\n\n")
    mailer.send_mail()
