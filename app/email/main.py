# templating example: https://justjensen.co/reporting-data-102-auto-emailing-reports-with-python-mjml-and-gmail/
from Mailer import Mailer
from getpass import getpass

import sys

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print(len(sys.argv))
        print("Parameters needed: <username>, <sender>, <receiver>")
        sys.exit()

    print("Number of arguments:", len(sys.argv), "arguments")
    print("Argument List:", str(sys.argv))

    # print("Please enter your Password: ", )
    password = getpass('Password:')

    mailer = Mailer(username=sys.argv[1], password=password, sender=sys.argv[2], receiver=sys.argv[3])
    # print(mailer.create_testmail())
    mailer.create_testmail("User")
    mailer.send_mail()
