from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.serializers.kennels import (
    KennelViewSerializer,
    KennelPhotoSerializer,
)
from catalog.serializers.breeds import BreedInKennelSerializer

from catalog.models import Kennel, BreedInKennel

from accounts.backends import get_token_payload, update_tokens_if_need



class KennelByIdView(APIView):
    @swagger_auto_schema(responses={200: KennelViewSerializer})
    def get(self, request, kennel_id):
        """получение данных заводчика по id,
        документация не полная, еще передается breeds [ {...}, {...}"""
        # todo документация - добавить breeds: [ {...}, {...} ]
        try:
            kennel = Kennel.objects.get(id=kennel_id)
        except ObjectDoesNotExist:
            return Response(
                data={f"заводчик {kennel_id} не найден"}, status=400
            )
        kennel_serializer = KennelViewSerializer(kennel, many=False)
        response_data = kennel_serializer.data

        try:
            breeds_in_kennel = BreedInKennel.objects.filter(kennel=kennel)
            breed_in_kennel_serializer = BreedInKennelSerializer(
                breeds_in_kennel, many=True, context={"request": request}
            )
            breeds_in_kennel_data = breed_in_kennel_serializer.data

        except ObjectDoesNotExist:
            # если нет пород, ассоциированных с питомником, возвращаем данные по питомнику без breeds
            return Response(status=200, data=response_data)

        # если есть хотя бы одна порода, добавляем ключ в словарь ответа и передаем с breeds
        breeds = [dict(ord_dict) for ord_dict in breeds_in_kennel_data]
        response_data["breeds"] = breeds

        return Response(status=200, data=response_data)


class KennelProfileView(APIView):
    @method_decorator(login_required)
    @swagger_auto_schema(responses={200: KennelViewSerializer})
    def get(self, request):
        """получение данных заводчика авторизованного пользователя.
        документация не полная, еще передается breeds [ {...}, {...}"""

        user_id = get_token_payload(request)["id"]

        try:
            kennel = Kennel.objects.get(user=user_id)
            kennel_serializer = KennelViewSerializer(
                kennel, many=False, context={"request": request}
            )
        except ObjectDoesNotExist:
            return Response(
                data={f"заводчик не найден (поиск по user_id из токена)"},
                status=400,
            )

        response_data = kennel_serializer.data

        try:
            breeds_in_kennel = BreedInKennel.objects.filter(kennel=kennel)
            breed_in_kennel_serializer = BreedInKennelSerializer(
                breeds_in_kennel, many=True, context={"request": request}
            )
            breeds_in_kennel_data = breed_in_kennel_serializer.data

        except ObjectDoesNotExist:
            # если нет пород, ассоциированных с питомником, возвращаем данные по питомнику без breeds
            return Response(status=200, data=response_data)

        # если есть хотя бы одна порода, добавляем ключ в словарь ответа и передаем с breeds
        breeds = [dict(ord_dict) for ord_dict in breeds_in_kennel_data]
        response_data["breeds"] = breeds
        response_data = dict(response_data, **update_tokens_if_need(request))
        return Response(status=200, data=response_data)

    @method_decorator(login_required)
    @swagger_auto_schema(
        request_body=KennelViewSerializer, responses={204: ""}
    )
    def put(self, request):
        """изменение данных заводчика авторизованного пользователя"""
        user_id = get_token_payload(request)["id"]
        try:
            kennel = Kennel.objects.get(user=user_id)
        except ObjectDoesNotExist:
            return Response(
                data={f"заводчик не найден (поиск по user_id из токена)"},
                status=400,
            )
        serializer = KennelViewSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.update(
            instance=kennel, validated_data=serializer.validated_data
        )
        return Response(status=204)


class KennelPhotoView(APIView):
    @method_decorator(login_required)
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_FILE, description="файл изображения"
        ),
        responses={204: ""},
    )
    def put(self, request):
        """добавление фото заводчика авторизованного пользователя"""
        user_id = get_token_payload(request)["id"]
        kennel = Kennel.objects.get(user=user_id)
        serializer = KennelPhotoSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.update(
            instance=kennel, validated_data=serializer.validated_data
        )
        return Response(status=204)

    @method_decorator(login_required)
    @swagger_auto_schema()
    def delete(self, request):
        """удаление фото заводчика авторизованного пользователя"""
        user_id = get_token_payload(request)["id"]
        Kennel.objects.get(user=user_id).photo.delete(save=True)
        return Response(status=204)
