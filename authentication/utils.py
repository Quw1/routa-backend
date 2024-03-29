from django.core.mail import send_mail


class Util:
    @staticmethod
    def send_email(data):
        send_mail(subject=data['email_subject'], message=data['email_body'], recipient_list=[data['email_to']], from_email='webmaster@localhost')
