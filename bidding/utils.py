# email sending class
from django.core.mail import EmailMessage
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(email, used_credit):
        email_body = f"Your auto bidding setup has passed the treshold and used {used_credit}$ of your credit"
        email_subject = "Auto Bidding Passed Treshold"
        email = EmailMessage(
            subject=email_subject, body=email_body, to=[email])
        EmailThread(email).start()
