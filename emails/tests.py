from django.test import TestCase
from users.models import CustomUser
from emails.views import Email


class EmailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(
            username="test_user",
            email="test@email.com",
            gender='male',
            age=26
        )
        user.set_password('secret')
        user.save()
        cls.user = user

    @staticmethod
    def _get_user_email():
        user = CustomUser.objects.get(username='test_user')
        return user.email

    # test sending email
    def test_sending_email(self):
        payload = {'subject': 'Test subject',
                   'message': 'Test message',
                   'receiver': self._get_user_email(),
                   'html': '<h1> Test Html>'
                   }
        email = Email.getInstance()
        response = email.send(payload)
        self.assertEqual(response, True)
