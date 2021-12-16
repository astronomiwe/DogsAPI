from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from config.settings import MEDIA_URL, MEDIA_ROOT


schema_view = get_schema_view(openapi.Info(title="Breederas API",
                                           default_version='v2.0',
                                           public=True
                                           )
                              )

ROOT_API_PATH = 'api/v2/'  # корневой путь для всех api, кроме admin

urlpatterns = [
    path('admin/', admin.site.urls),

    path(ROOT_API_PATH, include('catalog.urls')),
    path(ROOT_API_PATH, include('accounts.urls')),
    path(ROOT_API_PATH, include('articles.urls')),
    path(ROOT_API_PATH, include('feedback.urls')),
    # документация

    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)  # media

