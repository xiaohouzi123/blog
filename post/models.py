from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

# 文章
from redis import Redis


class Article(models.Model):
    uid = models.IntegerField(default=0)
    title = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    cilck = models.IntegerField(default=0)


# 评论
class Comment(models.Model):
    aid = models.IntegerField()
    uid = models.IntegerField(default=0)
    name = models.CharField(max_length=128, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

# 用户
class Users(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    # def verify_name(self,username):
    #     if username == self.name:
    #         return False
    #     else:
    #         return True
    #
    # def verify_pwd(self,password):
    #     if password == self.password:
    #         return True
    #     else:
    #         return False




