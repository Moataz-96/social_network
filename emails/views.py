from django.core.mail import send_mail
from config import settings


class Email:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Email.__instance is None:
            Email()
        return Email.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Email.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.sender = settings.DEFAULT_FROM_EMAIL
            Email.__instance = self

    def send(self, mail: dict):
        """
        :param
            mail: is a dict object of
                subject,
                message,
                receiver,
                html
        :return:
            True
        """
        send_mail(
            subject=mail['subject'],
            message=mail['message'],
            from_email=self.sender,
            recipient_list=[mail['receiver']],
            fail_silently=False,
            html_message=mail['html']
        )
        return True
