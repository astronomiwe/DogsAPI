from drf_yasg import openapi

announcement_request_params = [
    openapi.Parameter('date', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='дата', required=False),
    openapi.Parameter('kennel', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='id заводчика',
                      required=False),
    openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='страница', required=False),
]