from django.db import models


# Create your models here.

class Message(models.Model):
    username = models.CharField(max_length=255, verbose_name="用户名")
    room = models.CharField(max_length=255, verbose_name="聊天室")
    content = models.TextField(verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="写入时间")

class Users(models.Model):
    # 用户基本信息
    username = models.CharField(max_length=20,default=None,null=True)
    password = models.CharField(max_length=20,default=None,null=True)

    # 是否为管理员
    manager = models.BooleanField(default=False,blank=True,null=True)

    # 真实姓名
    real_name = models.CharField(max_length=20,default=None,null=True)
