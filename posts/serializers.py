# users/serializers.py

from rest_framework import serializers
from users.models import CustomUser
from posts.models import Post, PostLike


class UserExist(serializers.Serializer):
    pk = serializers.UUIDField(required=True, allow_null=False)

    def validate(self, attrs):
        validate_user = CustomUser.objects.filter(pk=attrs['pk'])
        if not validate_user.exists():
            raise serializers.ValidationError({
                'Error': 'User not found!'
            })
        attrs['user'] = validate_user[0]
        return attrs

    class Meta:
        fields = '__all__'


class PostExist(serializers.Serializer):
    pk = serializers.UUIDField(required=True, allow_null=False)

    def validate(self, attrs):
        validate_post = Post.objects.filter(pk=attrs['pk'])
        if not validate_post.exists():
            raise serializers.ValidationError({
                'Error': 'Post not found!'
            })
        attrs['post'] = validate_post[0]
        return attrs

    class Meta:
        fields = '__all__'


class PostDescValidator(serializers.Serializer):
    description = serializers.CharField(required=True, allow_null=False)

    class Meta:
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """ Custom representation """
        data = super().to_representation(instance)
        del data['is_active']
        data['likes'] = len(list(PostLike.objects.filter(post=instance, status=PostLike.LIKE)))
        data['unlikes'] = len(list(PostLike.objects.filter(post=instance, status=PostLike.UNLIKE)))
        return dict(data)

    class Meta:
        model = Post
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """ Custom representation """
        data = super().to_representation(instance)
        post = Post.objects.get(pk=data['post'])
        serializer = PostSerializer(instance=post, many=False)
        data = serializer.data
        return data

    class Meta:
        model = PostLike
        fields = '__all__'
        validators = []
