from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.auth import UserLoginSerializer, KennelSignupSerializer
from accounts.serializers.users import UserCredentialsViewSerializer
from catalog.serializers.breeds import BreedInKennelSerializer

from drf_yasg.utils import swagger_auto_schema

from catalog.models import Breed

from accounts.swagger.auth import signup_request_body, login_response_body


class Signup(APIView):
    """регистрация нового пользователя"""

    @swagger_auto_schema(request_body=signup_request_body, responses={201: ''})
    def post(self, request):
        # создание user
        try:
            user_serializer = UserCredentialsViewSerializer(data={'email': request.data.get('email'),
                                                              'password': request.data.get('password')
                                                              })
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.create(validated_data=user_serializer.validated_data)
            user.set_password(str(request.data.get('password')))
        except IntegrityError as error:
            return Response(status=400, data={"error": error.args[1]})

        try:
            # создание kennel
            kennel_serializer = KennelSignupSerializer(data={'title': request.data.get('title'),
                                                             'owner_name': request.data.get('owner_name'),
                                                             'phone': request.data.get('phone'),
                                                             'email': request.data.get('kennel_email'),
                                                             'user': user.id})
            kennel_serializer.is_valid(raise_exception=True)
            kennel = kennel_serializer.create(validated_data=kennel_serializer.validated_data)

        except IntegrityError as error:
            user.delete()
            return Response(status=400, data={"error": error.args[1]})

        try:
            # создание записей "порода у заводчика" (BreedInKennel)
            for breed_item in request.data.get('breeds'):
                breed = Breed.objects.get(name=breed_item['name'])
                breed_serializer = BreedInKennelSerializer(data={'breed': breed.name,
                                                                 'kennel': kennel.id
                                                                 })
                breed_serializer.is_valid(raise_exception=True)
                breed_serializer.create(validated_data=breed_serializer.validated_data)

        except IntegrityError as error:
            kennel.delete()
            user.delete()
            return Response(status=400, data={"error": error.args[1]})

        except ObjectDoesNotExist as error:
            kennel.delete()
            user.delete()
            return Response(status=400, data={"error": error.args})

        return Response(status=201)


class Login(APIView):
    """вход пользователя, получение токена"""

    @swagger_auto_schema(request_body=UserLoginSerializer,
                         responses={200: login_response_body})
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.validated_data, status=200)
