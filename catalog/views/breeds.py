from drf_yasg.utils import swagger_auto_schema
from catalog.swagger.breeds import breed_request_params, breed_response_body

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Breed
from catalog.serializers.breeds import BreedSerializer


class BreedView(APIView):
    @swagger_auto_schema(manual_parameters=breed_request_params, responses={200: breed_response_body})
    def get(self, request):
        """получение списка пород"""

        paginator = PageNumberPagination()

        breeds = Breed.objects.all()
        count = breeds.count()

        page = paginator.paginate_queryset(breeds, request)
        serializer = BreedSerializer(page, many=True, context={'request': request})

        return Response(status=200,
                        content_type="application/json; charset=UTF-8",
                        data={"total": count,
                              "records": serializer.data})
