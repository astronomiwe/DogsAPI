from drf_yasg import openapi

kennel_view_docs = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  properties={'avatar': openapi.Schema(type=openapi.TYPE_FILE,
                                                                       description='файл изображения'),
                                              'title': openapi.Schema(type=openapi.TYPE_STRING,
                                                                      description='название заводчика'),
                                              'owner_name': openapi.Schema(type=openapi.TYPE_STRING,
                                                                           description='имя заводчика'),
                                              'user': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                     description='id пользователя, '
                                                                                 'к которому привязан заводчик'),
                                              'phone': openapi.Schema(type=openapi.TYPE_STRING,
                                                                      description='телефон'),
                                              'email': openapi.Schema(type=openapi.TYPE_STRING,
                                                                      description='контактный е-майл'),
                                              'description': openapi.Schema(type=openapi.TYPE_STRING,
                                                                            description='описание'),
                                              'photo': openapi.Schema(type=openapi.TYPE_FILE,
                                                                      description='файл изображения'),
                                              'is_verified': openapi.Schema(type=openapi.TYPE_FILE,
                                                                            description='флаг '
                                                                                        '"подтвержденные документы"'),
                                              })

kennel_photo_docs = openapi.Schema(type=openapi.TYPE_OBJECT,
                                   properties={'photo': openapi.Schema(type=openapi.TYPE_FILE,
                                                                       description='файл изображения')})
