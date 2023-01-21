# users/views.py
from drf_spectacular.utils import extend_schema
from django.contrib.auth import login as login_auth
from rest_framework import permissions, status
from users.models import CustomUser
from users import serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from users.tasks import geolocation_info_task
from users import swagger
from services import utils
from emails.tasks import send_email
from allauth.account.admin import EmailAddress
from rest_framework_simplejwt.authentication import JWTAuthentication


@extend_schema(
    tags=["Users"],
    examples=swagger.filter_doc,
    responses={200: str, 400: str},
    request={"application/json": str},
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def filter(request):
    """
    Filter users by any key in the request body \n
    :param: \n
        None
    :body: \n
        {
            username [optional: String]: Username,
            email [optional: String]: Email account,
            gender [optional: String]: Male or Female,
            age [optional: Integer]: Age,
        }
    :return: \n
        List of objects
    """
    validator = serializers.UsersFiltersValidator(data=request.data)
    if validator.is_valid():
        filters = {f'{key}__exact': val for key, val in request.data.items()}
        data = CustomUser.objects.filter(**filters)
        serializer = serializers.UserSerializer(instance=data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Users"])
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def retrieve_active_users(request):
    """
    Retrieve all active users \n
    :param: \n
        None
    :body: \n
        None
    :return: \n
        List of objects
    """
    _users_obj = CustomUser.active.all()
    serializer = serializers.UserSerializer(instance=_users_obj, many=True)
    return Response(serializer.data, content_type="application/json", status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def retrieve_all_users(request):
    """
    Retrieve all users \n
    :param: \n
        None
    :body: \n
        None
    :return: \n
        List of objects
    """
    _users_obj = CustomUser.objects.all()
    serializer = serializers.UserSerializer(instance=_users_obj, many=True)
    return Response(serializer.data, content_type="application/json", status=status.HTTP_200_OK)


@extend_schema(
    tags=["Users"],
    responses={200: serializers.UserSerializer},
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def details(request, pk):
    """
    Retrieve user details by pk \n
    :param: \n
        id [required: String]: user uuid
            Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
    :body: \n
        None
    :return: \n
        User object details
    """
    validator = serializers.UserExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user = validator.validated_data['user']
    serializer = serializers.UserSerializer(instance=user, many=False)
    return Response(serializer.data, content_type="application/json", status=status.HTTP_200_OK)


@extend_schema(
    tags=["Users"],
    examples=swagger.update_doc,
    responses={200: str, 400: str},
    request={"application/json": serializers.UserSerializer},
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def update(request, pk):
    """
    Update users by any key in the request body \n
    :param: \n
        id [required: String]: user uuid
            Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
    :body: \n
        {
            username [optional: String]: Username,
            email [optional: String]: Email account,
            gender [optional: String]: Male or Female,
            age [optional: Integer]: Age,
        }
    :return: \n
        User object details after updated
    """
    validator = serializers.UserExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user = validator.validated_data['user']
    serializer = serializers.UserSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@extend_schema(
    tags=["Users"],
    responses={200: str, },
    request={"application/json": serializers.UserSerializer},
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def soft_delete(request, pk):
    """
    Delete user by de-activate account, user still exist but cannot login \n
    :param: \n
        id [required: String]: user uuid
            Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
    :body: \n
        None
    :return: \n
        message
    """
    validator = serializers.UserExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user = validator.validated_data['user']
    user.is_active = False
    user.save()
    return Response({"message": "User deleted successfully!"}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Users"],
    responses={200: str, },
    request={"application/json": serializers.UserSerializer},
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def hard_delete(request, pk):
    """
    Delete user account \n
    :param: \n
        id [required: String]: user uuid
            Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
    :body: \n
        None
    :return: \n
        message
    """
    validator = serializers.UserExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user = validator.validated_data['user']
    user.delete()
    return Response({"message": "User deleted successfully!"}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Users"],
    examples=swagger.change_password_doc,
    responses={200: str, 406: str},
    request={"application/json": serializers.UserSerializer},
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.AllowAny])
def change_password(request, pk):
    """
      Change password \n
      :param: \n
          id [required: String]: user uuid
              Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
      :body: \n
          {
              old_password [required: String]: old password,
              new_password1 [required: String]: new password,
              new_password2 [required: String]: new password,
          }
      :return: \n
          message
      """
    validator = serializers.UserExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user = validator.validated_data['user']
    request.data['user_password'] = user.password
    validate_changing_password = serializers.ChangePasswordSerializer(data=request.data)
    if not validate_changing_password.is_valid():
        return Response(validate_changing_password.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    user.password = validate_changing_password.validated_data['password']
    user.save()
    return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Users"],
    examples=swagger.login_doc,
    responses={200: str, 400: str},
    request={"application/json": serializers.UserSerializer},
)
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.AllowAny])
def login(request):
    """
      Login  \n
      :param: \n
          None
      :body: \n
          {
              username [required: String]: Username,
              password [required: String]: Password,
          }
      :return: \n
          {
            refresh: used for refresh token in case it expired
            access: for authentication
          }
      """
    validator = serializers.UserLoginValidator(data=request.data)
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user = validator.validated_data['user']
    login_auth(request, user)
    data = utils.get_tokens_for_user(user)
    code = status.HTTP_200_OK
    return Response(data, status=code)


@extend_schema(
    tags=["Users"],
    examples=swagger.signup_doc,
    responses={200: str, 406: str},
    request={"application/json": serializers.UserSerializer},
)
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.AllowAny])
def signup(request):
    """
      Signup  \n
      :param: \n
          None
      :body: \n
          {
              username [required: String]: Username,
              password1 [required: String]: Password,
              password2 [required: String]: Password,
              email [optional: String]: Password,
              gender [optional: Integer]: Password,
              age [optional: Integer]: Password,
          }
      :return: \n
          {
            refresh: used for refresh token in case it expired
            access: for authentication
          }
      """
    validator = serializers.UserSignUpValidator(data=request.data)
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    serializer = serializers.RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = CustomUser.objects.get(pk=serializer.data['id'])
        data = utils.get_tokens_for_user(user)
        send_email.apply_async(args=[user.id, 'verification'])
        current_date = user.date_joined.strftime("year=%Y&month=%m&day=%d")

        # Note: Running local will get local ip which will raise an exception with requests
        # For testing purposes, you can hard code your IP
        # ip = 'xx.xx.xx.xx' # Write your ip here

        ip = utils.get_client_ip(request)

        geolocation_info_task.apply_async(args=[ip, user.id, current_date])
        code = status.HTTP_200_OK
    else:
        data = serializer.errors
        code = status.HTTP_406_NOT_ACCEPTABLE
    return Response(data, status=code)


@extend_schema(tags=["Users"])
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.AllowAny])
def activate(request, pk):
    """
      Activate account \n
      :param: \n
          id [required: String]: user uuid
              Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
       :body: \n
          None
       :return: \n
          Message
       """
    validator = serializers.UserExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user = validator.validated_data['user']
    verified_email = EmailAddress.objects.filter(user_id=pk)
    if len(verified_email) > 0:
        return Response({"Details": "Account already verified"}, status.HTTP_400_BAD_REQUEST)
    EmailAddress.objects.create(user_id=pk, email=user.email, verified=True, primary=True)
    return Response({"Details": "Account verified!"}, status.HTTP_200_OK)
