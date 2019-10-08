from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(models.Model):
    """用户模型类"""
    nickname = models.CharField(max_length=256)
    username = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class OAuthQQUser(models.Model):
    """QQ登录用户"""
    user = models.ForeignKey('Users', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name