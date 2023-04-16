import os
from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from Binstragram.settings import MEDIA_ROOT
from .models import User
class Register(APIView):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        email = request.data.get('email', None)
        name = request.data.get('name', None)
        nickname = request.data.get('nickname', None)
        password = request.data.get('password', None)

        User.objects.create(email=email, name=name, nickname=nickname, password=make_password(password), profile_image="default_profile.png")

        return Response(status=200)

class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()    # filter는 리스트의 형태로 반환하기 때문.

        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # 로그인 체크 세션
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

class Logout(APIView):
    def get(self, request):
        # 세션 정보 초기화
        request.session.flush()
        return render(request, 'user/login.html')


class UploadProfile(APIView):
    def post(self, request):
        file = request.FILES['file']
        email = request.data.get('email')
        # 영어와 숫자로 이루어진 고유한 아이디(이름)을 주기 위해
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name

        user = User.objects.filter(email=email).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)

