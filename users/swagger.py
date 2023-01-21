from drf_spectacular.utils import OpenApiExample
filter_doc = [
    OpenApiExample(name="Request",
                   value={'username': "moataz",
                          'email': "moataz@gmail.com",
                          'gender': "male",
                          'age': 26,
                          },
                   request_only=True,
                   response_only=False,
                   ),
    OpenApiExample(name="Response",
                   status_codes=['200'],
                   value={'key': 'response'},
                   request_only=False,
                   response_only=True,
                   )
             ]

login_doc = [
    OpenApiExample(name="Request",
                   value={'username': "moataz",
                          'password': "123456"
                          },
                   request_only=True,
                   response_only=False,
                   ),
    OpenApiExample(name="Response",
                   status_codes=['200'],
                   value={'key': 'response'},
                   request_only=False,
                   response_only=True,
                   )
             ]


signup_doc = [
    OpenApiExample(name="Request",
                   value={'username': "moataz",
                          'password1': "123456",
                          'password2': "123456",
                          'email': "moataz@gmail.com",
                          'gender': "male",
                          'age': 26,
                          },
                   request_only=True,
                   response_only=False,
                   ),
    OpenApiExample(name="Response",
                   status_codes=['200'],
                   value={'key': 'response'},
                   request_only=False,
                   response_only=True,
                   )
             ]

change_password_doc = [
    OpenApiExample(name="Request",
                   value={'old_password': "123456",
                          'new_password1': "123456789",
                          'new_password2': "123456789"
                          },
                   request_only=True,
                   response_only=False,
                   )
    ]

update_doc = [
    OpenApiExample(name="Request",
                   value={'username': "moataz",
                          'password1': "123456",
                          'password2': "123456",
                          'email': "moataz@gmail.com",
                          'gender': "male",
                          'age': 26,
                          },
                   request_only=True,
                   response_only=False,
                   ),
    OpenApiExample(name="Response",
                   status_codes=['200'],
                   value={'username': "moataz",
                          'password1': "123456",
                          'password2': "123456",
                          'email': "moataz@gmail.com",
                          'gender': "male",
                          'age': 26,
                          },
                   request_only=False,
                   response_only=True,
                   )
]
refresh_token = [
    OpenApiExample(name="Request",
                   value={'refresh_token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NDMzOTc5MywiaWF0IjoxNjc0MjUzMzkzLCJqdGkiOiI0MDNkZjQ0NTgwYjQ0MjA4YjJiNWEzZmI3ZTZhMzk3YSIsInVzZXJfaWQiOiIxNjUxNmM5Yy0zOGM3LTQ4NjYtYjA4ZC0yOGM0MzBjYzkyZTEifQ.HvnZXIfmpya_zAN9sBhkHIWj7W2lSZ8m7fgQiQf-h2s",
                          },
                   request_only=True,
                   response_only=False,
                   ),
    OpenApiExample(name="Response",
                   status_codes=['200'],
                   value={'access_token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NDMzOTc5MywiaWF0IjoxNjc0MjUzMzkzLCJqdGkiOiI0MDNkZjQ0NTgwYjQ0MjA4YjJiNWEzZmI3ZTZhMzk3YSIsInVzZXJfaWQiOiIxNjUxNmM5Yy0zOGM3LTQ4NjYtYjA4ZC0yOGM0MzBjYzkyZTEifQ.HvnZXIfmpya_zAN9sBhkHIWj7W2lSZ8m7fgQiQf-h2s"
                          },
                   request_only=False,
                   response_only=True,
                   )
]