from drf_spectacular.utils import OpenApiExample

post_description = [
    OpenApiExample(name="Request",
                   value={'description': "Lorem Ipsum is simply dummy text of the "
                                         "printing and typesetting industry. "
                                         "Lorem Ipsum has been the industry's standard "
                                         "dummy text ever since the 1500s, "
                                         "when an unknown printer took a galley"},
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
