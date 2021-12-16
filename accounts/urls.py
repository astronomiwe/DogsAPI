from django.urls import path

from accounts.views.auth import Signup, Login
from accounts.views.users import UserCredentialsView, UserAvatarView

app_name = "accounts"

urlpatterns = [

    path('auth/signup/', Signup.as_view()),
    path('auth/login/', Login.as_view()),
    path('profile/user/', UserCredentialsView.as_view()),
    path('profile/user/avatar/', UserAvatarView.as_view())
]
