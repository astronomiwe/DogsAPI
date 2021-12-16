from rest_framework import serializers
from accounts.models import User
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import authenticate


class UserCredentialsViewSerializer(serializers.ModelSerializer):
    """сериализатор учетных данных пользователя"""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True, required=False
    )

    avatar = serializers.ImageField(required=False, use_url=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'avatar')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserAvatarSerializer(serializers.ModelSerializer):
    """сериализатор аватара"""
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ('avatar',)


class UserCredentialsChangeSerializer(serializers.ModelSerializer):
    """сериализатор изменения пользовательских данных
    """

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        required=True
    )
    new_password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True, required=False)

    new_email = serializers.EmailField(write_only=True, required=False)

    email = serializers.EmailField(required=False)

    def validate(self, data):

        password = data.get('password', None)
        new_email = data.get('new_email', None)
        new_password = data.get('new_password', None)

        if password is None:
            raise serializers.ValidationError(
                'Не введен текущий пароль'
            )

        # нужно получить email для последующей проверки правильности пароля
        email = data.get('email', None)
        user = authenticate(username=email, password=password)

        # проверка существования пользователя c таким email и паролем
        if user is None:
            raise serializers.ValidationError(
                f'Неправильный e-mail или пароль.'
            )

        if new_email is None and new_password is None:
            raise serializers.ValidationError("должен быть передан new_email или new_password")

        return {"email": new_email} if new_email else {"new_password": new_password}

    class Meta:
        model = User
        fields = ('email', 'password', 'new_password', 'new_email')
