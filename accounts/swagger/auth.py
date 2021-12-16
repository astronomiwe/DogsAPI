from drf_yasg import openapi

signup_request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                     properties={'email': openapi.Schema(type=openapi.FORMAT_EMAIL,
                                                                         description='регистрационный e-mail'),
                                                 'password': openapi.Schema(type=openapi.TYPE_STRING,
                                                                            description='пароль'),
                                                 'title': openapi.Schema(type=openapi.TYPE_STRING,
                                                                         description='название питомника'),
                                                 'owner_name': openapi.Schema(type=openapi.TYPE_STRING,
                                                                              description='имя заводчика'),
                                                 'phone': openapi.Schema(type=openapi.TYPE_STRING,
                                                                         description='контактный телефон'),
                                                 'kennel_email': openapi.Schema(type=openapi.TYPE_STRING,
                                                                         description='контактный емайл'),

                                                 'breeds': openapi.Schema(
                                                     type=openapi.TYPE_ARRAY,
                                                     items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                                         "name": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                description='название породы')}))
                                                 })

login_response_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                     properties={'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                                                 'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                                                 'user_id': openapi.Schema(type=openapi.TYPE_STRING,
                                                                           description='base64')
                                                 })
