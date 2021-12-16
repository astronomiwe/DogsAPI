from drf_yasg import openapi

breed_request_params = [
    openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='страница')
]

# здесь вручную переписаны поля сериализатора BreedSerializer
breed_response_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                     properties={'count': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                         description='количество записей'),
                                                 'records': openapi.Schema(
                                                     type=openapi.TYPE_ARRAY,
                                                     items=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                                          properties={
                                                                              'name': openapi.Schema(
                                                                                  type=openapi.TYPE_STRING,
                                                                                  description='название породы')}))
                                                 }
                                     )
