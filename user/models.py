from django.db import models
from django.contrib.auth import password_validation
# 用于加密保存密码
from django.contrib.auth.hashers import make_password
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=254)
    head = models.ImageField()
    age = models.IntegerField()
    sex = models.IntegerField()


