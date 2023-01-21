from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from config import settings
import jwt


def get_client_ip(request):
    """
    :param user: request object
    :return:
        - ip: user ip that has originated from the request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_tokens_for_user(user):
    """
    :param user: user object
    :return:
        - refresh: Bearer Token
        - access: Bearer Token
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_user_from_token(token):
    """
    :param token: request.auth
    :return:
        - user id: in case valid token
        - None: in case not valid
            it wouldn't face such a case,
            it would raise 401 error from IsAuthenticated decorator
    """

    try:
        algorithm = settings.SIMPLE_JWT['ALGORITHM']
        signing_key = settings.SIMPLE_JWT['SIGNING_KEY']
        payload = jwt.decode(str(token), signing_key, algorithm)
        user_id = payload.get("user_id")
        return user_id
    except jwt.DecodeError:
        return None
