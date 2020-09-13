from django.core.mail import EmailMessage
from django.core.mail import send_mail


class Util:
    @staticmethod
    def send_email(data):
        with mail.get_connection() as connection:
            mail.EmailMessage(
                subject=data['email_subject'], body=data['email_body'], to=[data['to_email']]).send()
