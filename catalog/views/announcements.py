from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema
from catalog.swagger.announcements import announcement_request_params

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView


from catalog.models import Announcement, Kennel, Breed

from catalog.serializers.announcements import (
    AnnouncementGetSerializer,
    AnnouncementPostSerializer,
    AnnouncementPostPutSerializer,
    PetPhotoSerializer,
    ParentPhotoSerializer,
)

from accounts.backends import get_token_payload, update_tokens_if_need

from config.urls import ROOT_API_PATH



class AnnouncementView(APIView):
    @swagger_auto_schema(
        manual_parameters=announcement_request_params,
        responses={200: AnnouncementGetSerializer},
    )
    def get(self, request):
        """
        получение списка обьявлений
        """

        date = request.GET.get("date", None)
        kennel = request.GET.get("kennel", None)

        if date and kennel:
            announcements = Announcement.objects.filter(
                created_at__gte=date, kennel=kennel
            ).all()
        elif date:
            announcements = Announcement.objects.filter(
                created_at__gte=date
            ).all()
        elif kennel:
            announcements = Announcement.objects.filter(kennel=kennel).all()
        elif not date and not kennel:
            announcements = Announcement.objects.all()

        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(announcements, request)

        serializer = AnnouncementGetSerializer(
            page, many=True, context={"request": request}
        )
        count = announcements.count()
        return Response(
            status=200,
            content_type="application/json; charset=UTF-8",
            data={"total": count,
                  "records": serializer.data},
        )

    @method_decorator(login_required)
    @swagger_auto_schema(
        request_body=AnnouncementGetSerializer, responses={201: ""}  # в документацию пробрасываем другой сериализатор
    )
    def post(self, request):
        """
        добавление обьявления от авторизованного пользователя.
        """
        user_id = get_token_payload(request)["id"]
        kennel = Kennel.objects.get(user=user_id)

        # предобработка названия породы для сериализатора (в модели и сериализаторе используется id)
        breed = Breed.objects.get(name=request.data.get("breed"))

        announcement_serializer = AnnouncementPostSerializer(
            data={
                "title": request.data.get("title"),
                "kennel": kennel.id,
                "breed": breed.name,
                "male_count": request.data.get("male_count"),
                "female_count": request.data.get("female_count"),
                "birthday": request.data.get("birthday"),
                "with_documents": request.data.get("with_documents"),
                "price": request.data.get("price"),
                "city": request.data.get("city"),
                "is_transportable": request.data.get("is_transportable"),
                "description": request.data.get("description"),
                "parents_description": request.data.get("parents_description"),
            }
        )
        announcement_serializer.is_valid(raise_exception=True)
        announcement = announcement_serializer.create(
            validated_data=announcement_serializer.validated_data
        )

        # создание фотографий питомца, проассоциированных с id обьявления
        if request.data.get("pet_photos"):
            for pet_photo_item in request.data.get("pet_photos"):
                pet_photo_serializer = PetPhotoSerializer(
                    data={
                        "announcement": announcement.id,
                        "image": pet_photo_item["image"],
                    }
                )
                pet_photo_serializer.is_valid(raise_exception=True)
                pet_photo_serializer.create(
                    validated_data=pet_photo_serializer.validated_data
                )

        # создание фотографий родителей, проассоциированных с id обьявления
        if request.data.get("parent_photos"):
            for parent_photo_item in request.data.get("parent_photos"):
                parent_photo_serializer = ParentPhotoSerializer(
                    data={
                        "announcement": announcement.id,
                        "image": parent_photo_item["image"],
                    }
                )
                parent_photo_serializer.is_valid(raise_exception=True)
                parent_photo_serializer.create(
                    validated_data=parent_photo_serializer.validated_data
                )

        return Response(
            status=201,
            content_type="application/json; charset=UTF-8",
            headers={
                "Location": f"{ROOT_API_PATH}announcements/{announcement.id}/"
            },
        )


class AnnouncementByIdView(APIView):
    @swagger_auto_schema(responses={200: AnnouncementGetSerializer})
    def get(self, request, announcement_id):
        """получение обьявления по id"""
        try:
            announcement = Announcement.objects.get(id=announcement_id)
            serializer = AnnouncementGetSerializer(
                announcement, many=False, context={"request": request}
            )
            return Response(
                status=200,
                content_type="application/json; charset=UTF-8",
                data={"total": 1, "records": serializer.data},
            )
        except ObjectDoesNotExist:
            return Response(
                status=404,
                content_type="text/plain; charset=UTF-8",
                data=f'Обьявление с  "{announcement_id = }" не найдено',
            )

    @method_decorator(login_required)
    @swagger_auto_schema(
        request_body=AnnouncementPostPutSerializer, responses={204: ""}
    )
    def put(self, request, announcement_id):
        """изменение данных обьявления авторизованного пользователя по id
        (метод еще не реализован)"""
        # фронт передает все данные, не зависимо от того, поменял пользователь значение или нет
        user_id = get_token_payload(request)["id"]
        try:
            kennel_id = Kennel.objects.get(user=user_id).id
            Announcement_data = Announcement.objects.get(
                kennel=kennel_id, id=announcement_id
            )
        except ObjectDoesNotExist:
            return Response(
                data={f"обьявление не найдено или не принадлежит авторизованному пользователю"},
                status=404,
            )
        if request.method == 'PUT':
            announcement = request.data.get(Announcement_data)
            announcement_serializer = AnnouncementPostPutSerializer(Announcement_data, data=announcement)
            if announcement_serializer.is_valid(raise_exception=True):
                announcement_serializer.save()
                return Response(status=204)
            return Response(
                announcement_serializer.errors, status=400
            )

        # #  прописать data= вручную для announcement,
        # #  и data и логику наполнения фоток (по id, если фотка существует в базе)
        # # AnnouncementUpdateSerializer - только в доках
        # serializer = AnnouncementPostPutSerializer(data=request.data, many=False)
        # serializer.is_valid(raise_exception=True)
        # serializer.update(
        #     instance=announcement, validated_data=serializer.validated_data
        # )
        # return Response(status=204)

    @method_decorator(login_required)
    @swagger_auto_schema()
    def delete(self, request, announcement_id):
        """удаление обьявления авторизованного пользователя по id"""
        user_id = get_token_payload(request)["id"]
        try:
            kennel_id = Kennel.objects.get(user=user_id).id
            Announcement.objects.get(
                id=announcement_id, kennel=kennel_id
            ).delete()
            return Response(status=204)
        except ObjectDoesNotExist:
            return Response(
                status=404,
                content_type="text/plain; charset=UTF-8",

            )


class AnnouncementProfileView(APIView):
    @method_decorator(login_required)
    @swagger_auto_schema(responses={200: AnnouncementGetSerializer})
    def get(self, request):
        """получение обьявлений авторизованного пользователя"""

        user_id = get_token_payload(request)["id"]
        kennel_id = Kennel.objects.get(user=user_id)
        announcements = Announcement.objects.filter(kennel=kennel_id).all()

        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(announcements, request)

        serializer = AnnouncementGetSerializer(
            page, many=True, context={"request": request}
        )
        count = announcements.count()
        response_data = dict({"total": count,
                              "records": serializer.data},
                             **update_tokens_if_need(request))
        return Response(
            status=200,
            content_type="application/json; charset=UTF-8",
            data=response_data
        )
