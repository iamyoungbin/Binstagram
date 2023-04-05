import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from Binstragram.settings import MEDIA_ROOT
from .models import Feed

# Create your views here.
class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id')  # == select * from Feed; (sql)

        print(request.session['email'])
        email = request.session['email']
        # 로그인 없이 메인에 접근하는 경우
        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=request.session['email']).first()

        # 회원이 아닌 이메일 주소인 경우
        if user is None:
            return render(request, "user/login.html")

        return render(request, "binstagram/main.html", context=dict(feeds=feed_list, user=user))

class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']
        # 영어와 숫자로 이루어진 고유한 아이디(이름)을 주기 위해
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0)

        return Response(status=200)