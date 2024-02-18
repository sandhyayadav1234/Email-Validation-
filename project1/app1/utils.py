from django.core.mail import EmailMessage
from django.conf import settings
import os

class Utils:
    @staticmethod
    def send_Email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_mail']]
        )
        email.send()
        