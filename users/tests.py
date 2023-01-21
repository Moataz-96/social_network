from django.test import TestCase
from users.models import CustomUser
from rest_framework.authtoken.models import Token
from services import utils

class UsersTests(TestCase):
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
    def _get_token():
        user = CustomUser.objects.get(username='test_user')
        token = utils.get_tokens_for_user(user)
        access = token['access']
        return f'Bearer {access}'

    @staticmethod
    def _get_pk():
        user = CustomUser.objects.get(username='test_user')
        return user.id

    # test signup user
    def test_signup(self):
        payload = {'username': "test_signup",
                   'password1': "123456",
                   'password2': "123456",
                   'email': "test_signup@gmail.com",
                   'gender': "male",
                   'age': 26}
        response = self.client.post(f"/api/users/signup/", data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    # test login user
    def test_login(self):
        payload = {'username': "test_user",
                   'password': "secret"}
        response = self.client.post(f"/api/users/login/", data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    # test filter users
    def test_filter(self):
        payload = {'username': 'test_user'}
        response = self.client.post(f"/api/users/filter/",
                                    data=payload, content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test retrieve all users
    def test_all(self):
        response = self.client.post(f"/api/users/all/",
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test retrieve active users
    def test_active(self):
        response = self.client.post(f"/api/users/active/",
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test retrieve user details
    def test_details(self):
        pk = self._get_pk()
        response = self.client.post(f"/api/users/details/{pk}/",
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test update user
    def test_update(self):
        pk = self._get_pk()
        payload = {'email': 'email@gmail.com'}
        response = self.client.put(f"/api/users/update/{pk}/",
                                   data=payload, content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test soft delete user
    def test_soft_delete(self):
        pk = self._get_pk()
        response = self.client.delete(f"/api/users/delete/soft/{pk}/",
                                      content_type="application/json",
                                      **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test hard delete user
    def test_hard_delete(self):
        pk = self._get_pk()
        response = self.client.delete(f"/api/users/delete/hard/{pk}/",
                                      content_type="application/json",
                                      **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)
        self.setUpTestData()  # Re-Create the user

    # test change user password
    def test_change_password(self):
        pk = self._get_pk()
        payload = {'old_password': "secret",
                   'new_password1': "secret",  # fake new password
                   'new_password2': "secret"
                   }
        response = self.client.post(f"/api/users/change_password/{pk}/",
                                    data=payload, content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)
