from django.urls import path
from .views import UploadFeed, Profile, UploadReply

urlpatterns = [
    path('upload/', UploadFeed.as_view()),
    path('profile/', Profile.as_view()),
    path('reply/', UploadReply.as_view()),
]