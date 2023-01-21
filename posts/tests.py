from django.test import TestCase
from users.models import CustomUser
from posts.models import Post
from services import utils
from django.contrib.auth.hashers import make_password


class UsersTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user, _ = CustomUser.objects.get_or_create(
            username="test_user",
            password=make_password('secret'),
            email="test@email.com",
            gender='male',
            age=26
        )

        cls.post, _ = Post.objects.get_or_create(
            user=cls.user,
            description="test post description"
        )

    @staticmethod
    def _get_token():
        user = CustomUser.objects.get(username='test_user')
        token = utils.get_tokens_for_user(user)
        access = token['access']
        return f'Bearer {access}'

    @staticmethod
    def _get_user_pk():
        user = CustomUser.objects.get(username='test_user')
        return user.id

    @staticmethod
    def _get_post_pk():
        post = Post.objects.get(user=UsersTests._get_user_pk())
        return post.id

    # test create post
    def test_create(self):
        payload = {'description': "test_post"}
        response = self.client.post(f"/api/posts/create/",
                                    data=payload, content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test retrieve post
    def test_retrieve(self):
        response = self.client.get(f"/api/posts/retrieve/{self._get_post_pk()}/",
                                   content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test update post
    def test_update(self):
        payload = {'description': 'new description'}
        response = self.client.put(f"/api/posts/update/{self._get_post_pk()}/",
                                   data=payload, content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test soft delete user
    def test_soft_delete(self):
        pk = self._get_post_pk()
        response = self.client.delete(f"/api/posts/delete/soft/{pk}/",
                                      content_type="application/json",
                                      **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test retrieve all posts
    def test_all(self):
        response = self.client.post(f"/api/posts/all/",
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test retrieve active posts
    def test_active(self):
        response = self.client.post(f"/api/posts/active/",
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test retrieve user posts
    def test_user_posts(self):
        response = self.client.post(f"/api/posts/user/{self._get_user_pk()}/",
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test post contains
    def test_contains(self):
        payload = {'description': 'description'}
        response = self.client.post(f"/api/posts/contains/",
                                    data=payload, content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test post like
    def test_like(self):
        response = self.client.post(f"/api/posts/{self._get_post_pk()}/status/like/",
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test post unlike
    def test_unlike(self):
        response = self.client.post(f"/api/posts/{self._get_post_pk()}/status/unlike/",
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test post remove like or remove unlike
    def test_default(self):
        response = self.client.post(f"/api/posts/{self._get_post_pk()}/status/default/",
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)

    # test hard delete user
    def test_two_hard_delete(self):
        pk = self._get_post_pk()
        response = self.client.delete(f"/api/posts/delete/hard/{pk}/",
                                      content_type="application/json",
                                      **{'HTTP_AUTHORIZATION': self._get_token()})
        self.assertEqual(response.status_code, 200)
