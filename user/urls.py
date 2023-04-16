from django.contrib import admin
from django.urls import path
from .views import Register, Login, Logout, UploadProfile

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('profile/upload/', UploadProfile.as_view()),
]