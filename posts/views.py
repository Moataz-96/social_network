# users/views.py
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from posts import serializers
from posts.models import Post, PostLike
from users.models import CustomUser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from services import utils
from posts import swagger


@extend_schema(
    tags=["Posts"],
    examples=swagger.post_description,
    responses={200: str, 400: str},
    request={"application/json": str},
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def contains(request):
    """
      Retrieve all posts that contains any word \n
      :param: \n
          None
      :body: \n
          {
              description [required: String]: 'text'
          }
      :return: \n
          List of posts objects
      """
    validator = serializers.PostDescValidator(data=request.data)
    if validator.is_valid():
        data = Post.objects.filter(description__contains=validator.validated_data['description'])
        serializer = serializers.PostSerializer(instance=data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Posts"])
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def retrieve_active_posts(request):
    """
      Retrieve all active posts \n
      :param: \n
          None
      :body: \n
          None
      :return: \n
          List of posts objects
      """
    _post_obj = Post.active.all()
    serializer = serializers.PostSerializer(instance=_post_obj, many=True)
    return Response(serializer.data, content_type="application/json", status=status.HTTP_200_OK)


@extend_schema(tags=["Posts"])
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def retrieve_all_posts(request):
    """
      Retrieve all posts \n
      :param: \n
          None
      :body: \n
          None
      :return: \n
          List of posts objects
      """
    _post_obj = Post.objects.all()
    serializer = serializers.PostSerializer(instance=_post_obj, many=True)
    return Response(serializer.data, content_type="application/json", status=status.HTTP_200_OK)


@extend_schema(
    tags=["Posts"],
    responses={200: serializers.PostSerializer},
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def retrieve_user_posts(request, pk):
    """
      Retrieve all posts of user \n
      :param: \n
          id [required: String]: user uuid
              Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
      :body: \n
          None
      :return: \n
          List of posts objects
      """
    validator = serializers.UserExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user = validator.validated_data['user']
    data = Post.objects.filter(user=user)
    serializer = serializers.PostSerializer(instance=data, many=True)
    return Response(serializer.data, content_type="application/json", status=status.HTTP_200_OK)


@extend_schema(
    tags=["Posts"],
    examples=swagger.post_description,
    responses={200: str, 400: str},
    request={"application/json": serializers.PostSerializer},
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def create(request):
    """
      Create new post for the authenticated user \n
      :param: \n
          None
      :body: \n
          {
              description [required: String]: 'text'
          }
      :return: \n
          List of posts objects
      """
    request.data['user'] = utils.get_user_from_token(request.auth)
    serializer = serializers.PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@extend_schema(
    tags=["Posts"],
    responses={200: str, },
    request={"application/json": serializers.PostSerializer},
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def retrieve(request, pk):
    """
      Retrieve details of post by id \n
      :param: \n
          id [required: String]: post uuid
              Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
      :body: \n
          None
      :return: \n
          List of posts objects
      """
    validator = serializers.PostExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    post = validator.validated_data['post']
    serializer = serializers.PostSerializer(instance=post, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Posts"],
    examples=swagger.post_description,
    responses={200: str, 400: str},
    request={"application/json": serializers.PostSerializer},
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def update(request, pk):
    """
      Update post \n
      :param: \n
          id [required: String]: post uuid
              Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
      :body: \n
          {
              description [required: String]: 'text'
          }
      :return: \n
          Updated post object
      """
    request.data['user'] = utils.get_user_from_token(request.auth)
    validator = serializers.PostExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    post = validator.validated_data['post']
    serializer = serializers.PostSerializer(instance=post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@extend_schema(
    tags=["Posts"],
    responses={200: str, },
    request={"application/json": serializers.PostSerializer},
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def soft_delete(request, pk):
    """
    Delete post by de-activate post, post still exist but cannot be viewed \n
    :param: \n
        id [required: String]: user uuid
            Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
    :body: \n
        None
    :return: \n
        message
    """
    validator = serializers.PostExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    post = validator.validated_data['post']
    post.is_active = False
    post.save()
    return Response({"message": "Post deleted successfully!"}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Posts"],
    responses={200: str, },
    request={"application/json": serializers.PostSerializer},
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def hard_delete(request, pk):
    """
    Delete post  \n
    :param: \n
        id [required: String]: user uuid
            Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
    :body: \n
        None
    :return: \n
        message
    """
    validator = serializers.PostExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    post = validator.validated_data['post']
    post.delete()
    return Response({"message": "Post deleted successfully!"}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Posts"],
    responses={200: str, 400: str},
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def status_like(request, pk):
    """
    Like post endpoint for the authenticated use  \n
    :param: \n
        id [required: String]: user uuid
            Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
    :body: \n
        None
    :return: \n
        Post object details
    """
    validator = serializers.PostExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user_id = utils.get_user_from_token(request.auth)
    user = CustomUser.objects.get(id=user_id)
    post = validator.validated_data['post']
    post_likes, created = PostLike.objects.update_or_create(
        user=user,
        post=post,
        defaults={'status': PostLike.LIKE}
    )
    serializer = serializers.PostLikeSerializer(instance=post_likes)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Posts"],
    responses={200: str, 400: str},
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def status_unlike(request, pk):
    """
    Unlike post endpoint for the authenticated use  \n
    :param: \n
        id [required: String]: user uuid
            Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
    :body: \n
        None
    :return: \n
        Post object details
    """
    validator = serializers.PostExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user_id = utils.get_user_from_token(request.auth)
    user = CustomUser.objects.get(id=user_id)
    post = validator.validated_data['post']
    post_likes, created = PostLike.objects.update_or_create(
        user=user,
        post=post,
        defaults={'status': PostLike.UNLIKE}
    )
    serializer = serializers.PostLikeSerializer(instance=post_likes)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Posts"],
    responses={200: str, 400: str}
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def status_default(request, pk):
    """
    Remove like/unlike on post endpoint for the authenticated use  \n
    :param: \n
        id [required: String]: user uuid
            Example: c5aa0975-050b-45d4-8b2b-13e35a40ea4a
    :body: \n
        None
    :return: \n
        Post object details
    """
    validator = serializers.PostExist(data={'pk': pk})
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_404_NOT_FOUND)
    user_id = utils.get_user_from_token(request.auth)
    user = CustomUser.objects.get(id=user_id)
    post = validator.validated_data['post']
    post_likes, created = PostLike.objects.update_or_create(
        user=user,
        post=post,
        defaults={'status': PostLike.DEFAULT}
    )
    serializer = serializers.PostLikeSerializer(instance=post_likes)
    post_likes.delete()
    return Response(serializer.data, status=status.HTTP_200_OK)
