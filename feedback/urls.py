from django.urls import path

from feedback.views import FeedbackView

urlpatterns = [
    path('feedback/', FeedbackView.as_view(), name='contact'),

]