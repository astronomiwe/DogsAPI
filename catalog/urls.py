from django.urls import path

from catalog.views.announcements import AnnouncementByIdView, AnnouncementView, AnnouncementProfileView
from catalog.views.breeds import BreedView
from catalog.views.kennels import KennelByIdView, KennelProfileView, KennelPhotoView

app_name = "catalog"

urlpatterns = [
    path('announcements/<int:announcement_id>/', AnnouncementByIdView.as_view()),
    path('announcements/', AnnouncementView.as_view()),

    path('breeds/', BreedView.as_view()),

    path('kennel/<int:kennel_id>', KennelByIdView.as_view()),

    path('profile/kennel/', KennelProfileView.as_view()),
    path('profile/kennel/photo/', KennelPhotoView.as_view()),
    path('profile/announcements/', AnnouncementProfileView.as_view())
]
