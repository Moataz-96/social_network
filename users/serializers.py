# users/serializers.py

from rest_framework import serializers
from users.models import CustomUser, UserHolidays
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate


class UsersFiltersValidator(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256, required=False, allow_null=True, validators=[])

    class Meta:
        model = CustomUser
        fields = '__all__'
        validators = []
        extra_kwargs = {field.name: {"required": False, "allow_null": True}
                        for field in CustomUser._meta.get_fields()}


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


class UserLoginValidator(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True, allow_null=False)
    password = serializers.CharField(max_length=256, required=True, allow_null=False)

    def validate(self, attrs):
        validate_user = authenticate(username=attrs['username'], password=attrs['password'])
        if not validate_user:
            raise serializers.ValidationError({
                'User': 'Incorrect username or password!'
            })
        if not validate_user.is_active:
            raise serializers.ValidationError({
                'User': 'User deleted!'
            })
        attrs['user'] = validate_user
        return attrs

    class Meta:
        fields = '__all__'


class UserSignUpValidator(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True, allow_null=False)
    email = serializers.EmailField(required=True, allow_null=False)
    password1 = serializers.CharField(max_length=256, required=True, allow_null=False)
    password2 = serializers.CharField(max_length=256, required=True, allow_null=False)

    def validate(self, attrs):
        validate_username = CustomUser.objects.filter(username=attrs['username']).exists()
        validate_email = CustomUser.objects.filter(email=attrs['email']).exists()
        validate_password = (attrs['password1'] == attrs['password2'])

        if validate_username:
            raise serializers.ValidationError({
                'username': 'Username already exists!'
            })
        if validate_email:
            raise serializers.ValidationError({
                'email': 'Email already exists!'
            })

        if not validate_password:
            raise serializers.ValidationError({
                'password': 'Passwords not matching!'
            })
        return True

    class Meta:
        fields = '__all__'


class UserHolidaysSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """ Dict response """
        data = super().to_representation(instance)
        return dict(data)

    class Meta:
        model = UserHolidays
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """ Dict response """
        data = super().to_representation(instance)
        user = CustomUser.objects.get(id=data['pk'])
        instance = UserHolidays.objects.filter(user=user)
        user_holidays = UserHolidaysSerializer(instance=instance, many=True)
        data['holidays'] = user_holidays.data
        return dict(data)

    class Meta:
        fields = (
            'pk',
            "username",
            "email",
            "first_name",
            "last_name",
            'gender',
            'age',
        )
        model = CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(read_only=True)
    password2 = serializers.CharField(read_only=True)

    def to_internal_value(self, data):
        data['password'] = make_password(data['password1'])
        del data['password1']
        del data['password2']
        return data

    class Meta:
        fields = '__all__'
        model = CustomUser


class ChangePasswordSerializer(serializers.Serializer):
    user_password = serializers.CharField(required=True, allow_null=False)
    old_password = serializers.CharField(required=True, allow_null=False)
    new_password1 = serializers.CharField(required=True, allow_null=False)
    new_password2 = serializers.CharField(required=True, allow_null=False)

    def validate(self, attrs):
        validate_old_pass = check_password(attrs['old_password'], attrs['user_password'])
        if not validate_old_pass:
            raise serializers.ValidationError({
                'Password': 'Incorrect password!'
            })
        validate_matching = (attrs['new_password1'] == attrs['new_password2'])
        if not validate_matching:
            raise serializers.ValidationError({
                'Password': 'Passwords not matching!'
            })
        attrs['password'] = make_password(attrs['new_password1'])
        return attrs

    class Meta:
        fields = '__all__'
