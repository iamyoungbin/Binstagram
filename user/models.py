from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
class User(AbstractBaseUser):
    """
    유저 프로필 사진
    유저 아이디  => 닉네임
    유저 이메일 주소 => 회원가입 시 사용하는 아이디
    실제 사용자 이름 => default
    """

    profile_image = models.TextField()  # 길이 제한 없음
    nickname = models.CharField(max_length=24, unique=True) # 길이 제한 있음
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'nickname'
    class Meta:
        db_table = "User"