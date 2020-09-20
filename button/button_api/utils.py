from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError, send_mail
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response


class Util:
    @staticmethod
    def send_email(data):
        try:
            with mail.get_connection() as connection:
                mail.EmailMessage(
                    subject=data['email_subject'], body=data['email_body'], to=[data['to_email']]).send()
        except Exception:
            return Response("email not sent"+Exception)
