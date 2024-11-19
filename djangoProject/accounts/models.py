from django.db import models
from django.contrib.auth.models import AbstractUser

# 사용자 모델 정의
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30, blank=True, null=True)
    profile_img = models.ImageField(upload_to="profile_images/", default="images/profile_default.png")
    age = models.IntegerField(default=0)
    money = models.IntegerField(default=0)
    salary = models.IntegerField(default=0)