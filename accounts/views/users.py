from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from drf_yasg import openapi

from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.users import (UserCredentialsViewSerializer,
                                        UserAvatarSerializer,
                                        UserCredentialsChangeSerializer)

from accounts.models import User

from accounts.backends import get_token_payload

from accounts.backends import update_tokens_if_need


class UserCredentialsView(APIView):

    @method_decorator(login_required)
    @swagger_auto_schema(responses={200: UserCredentialsViewSerializer})
    def get(self, request):
        """
        получение данных текущего пользователя (для профиля).
        """

        user_id = get_token_payload(request)["id"]
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response(data={f'пользователь {user_id} не найден'}, status=400)
        serializer = UserCredentialsViewSerializer(user, many=False)
        response_data = dict(serializer.data, **update_tokens_if_need(request))
        return Response(status=200, data=response_data)

    @method_decorator(login_required)
    @swagger_auto_schema(request_body=UserCredentialsChangeSerializer, responses={204: ''})
    def put(self, request):
        """
        изменение данных текущего пользователя.
        Необходимо обязательно передать password и что меняем (new_email ИЛИ new_password).
        email передавать не нужно.
        """

        user_id = get_token_payload(request)["id"]

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response(data={f'пользователь {user_id} не найден'}, status=400)

        request_data = dict(request.data)
        request_data['email'] = user.email
        serializer = UserCredentialsChangeSerializer(data=request_data, many=False)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if 'email' in validated_data:
            serializer.update(instance=user, validated_data=validated_data)
        elif 'new_password' in validated_data:
            user.set_password(validated_data['new_password'])
            user.save()
        return Response(status=204)


class UserAvatarView(APIView):

    @method_decorator(login_required)
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_FILE,
                                                     description='файл изображения'), responses={204: ''})
    def put(self, request):
        """добавление аватара текущего пользователя"""

        user_id = get_token_payload(request)["id"]

        user = User.objects.get(id=user_id)

        serializer = UserAvatarSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user, validated_data=serializer.validated_data)

        return Response(status=204)

    @method_decorator(login_required)
    @swagger_auto_schema()
    def delete(self, request):
        """удаление аватара текущего пользователя"""

        user_id = get_token_payload(request)["id"]

        User.objects.get(id=user_id).avatar.delete(save=True)

        return Response(status=204)
