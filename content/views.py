import os
from uuid import uuid4

from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from Binstragram.settings import MEDIA_ROOT
from .models import Feed, Reply, Like, Bookmark

# Create your views here.
class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        # 로그인 없이 메인에 접근하는 경우
        if email is None:
            return redirect('/user/login/')
            # return render(request, "user/login.html")

        user = User.objects.filter(email=request.session['email']).first()

        # 회원이 아닌 이메일 주소인 경우
        if user is None:
            return redirect('/user/login/')
            # return render(request, "user/login.html")

        print(email)
        feed_object_list = Feed.objects.all().order_by('-id')  # == select * from Feed; (sql)
        feed_list = []

        for feed in feed_object_list:
            feed_user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                reply_user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=reply_user.nickname))

            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_bookmarked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()

            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=feed_user.profile_image,
                                  nickname=feed_user.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_bookmarked=is_bookmarked,))

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
        email = request.session.get('email', None)

        Feed.objects.create(image=image, content=content, email=email)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        # 로그인 없이 메인에 접근하는 경우
        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=request.session['email']).first()

        # 회원이 아닌 이메일 주소인 경우
        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email).all()
        liked_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        # value_list 를 통해 리스트에서 특정 value 값만 뽑아내 새로운 리스트 생성.
        liked_feed_list = Feed.objects.filter(id__in=liked_list).all()
        # id__in => python in 사용법과 동일.
        marked_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        marked_feed_list = Feed.objects.filter(id__in=marked_list).all()

        return render(request, "content/profile.html", context=dict(feed_list=feed_list,
                                                                    liked_feed_list=liked_feed_list,
                                                                    marked_feed_list=marked_feed_list,
                                                                    user=user))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id,
                             reply_content=reply_content,
                             email=email, )

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_state = request.data.get('favorite_state', True)
        email = request.session.get('email', None)

        if favorite_state == 'favorite':
            # jquery로 boolean 값이 넘어오지 않기 때문에
            is_like = True
        else:
            is_like = False

        like = Like.objects.filter(email=email, feed_id=feed_id).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_state = request.data.get('bookmark_state', True)
        email = request.session.get('email', None)

        if bookmark_state == 'bookmark':
            # jquery로 boolean 값이 넘어오지 않기 때문에
            is_marked = True
        else:
            is_marked = False

        bookmark = Bookmark.objects.filter(email=email, feed_id=feed_id).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)
