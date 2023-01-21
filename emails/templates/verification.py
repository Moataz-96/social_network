from emails.templates.template import Template
from emails.views import Email
from config import settings
from users.models import CustomUser


class Verification(Template):
    def __init__(self):
        self.email = Email.getInstance()

    def prepare_template(self, data):
        return {
          'subject': 'Email Activation',
          'message': "Welcome to Social Network",
          'receiver': data['email'],
          'html': f'''
                <h1>Please Activate your account</h1>
                <a href={data['url']}>Activate now</a>
                '''
        }

    def send(self, user: CustomUser) -> None:
        """
        Send activation email for users
        :param user: CustomUser Object
        :return:
            Boolean: True if email send successfully
        """
        data = {
            'url': f"{settings.domain}/api/users/activate/{user.id}/",
            'email': user.email
            }
        template = self.prepare_template(data)
        self.email.send(template)
