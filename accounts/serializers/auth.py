from rest_framework import serializers

from django.contrib.auth import authenticate

from accounts.models import User

from catalog.models import Kennel

import base64


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    user_id = serializers.CharField(read_only=True, label='base64')

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        # Вызвать исключение, если не предоставлена почта.
        if email is None:
            raise serializers.ValidationError("Для входа нужен e-mail")

        # Вызвать исключение, если не предоставлен пароль.
        if password is None:
            raise serializers.ValidationError("Для входа нужен пароль")

        # передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.
        user = authenticate(username=email, password=password)

        # проверка существования пользователя
        if user is None:
            raise serializers.ValidationError(
                f"Неправильный e-mail или пароль."
            )

        # проверка активного пользователя
        if not user.is_active:
            raise serializers.ValidationError("Пользователь заблокирован.")

        # user.id > base64 для google analytics
        user_id_str = str(user.id)
        uid_in_base64 = base64.b64encode(user_id_str.encode("UTF-8"))

        return {"access_token": user.access_token,
                "user_id": uid_in_base64,
                "refresh_token": user.refresh_token}

    class Meta:
        model = User
        fields = ("email", "password", "access_token", "refresh_token", "user_id")


class KennelSignupSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    owner_name = serializers.CharField(required=True)

    class Meta:
        model = Kennel
        fields = ("title", "owner_name", "phone", "user", "email")
