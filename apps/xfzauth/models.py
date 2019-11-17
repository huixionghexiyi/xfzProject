# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models
# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError("请输入手机号")
        if not username:
            raise ValueError("请输入用户名")
        if not password:
            raise ValueError("请输入密码")
        user = self.model(telephone=telephone,
                          username=username, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 不要使用自增长的主键
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    # password 我猜测不需要重写,因为AbstractBaseUser内置的就可以了。需要看鉴权和授权
    # password = models.CharField(max_length=200)
    email = models.EmailField(unique=True,null=True)
    username = models.CharField(max_length=100)
    # 是否可用
    is_active = models.BooleanField(default=True)
    # 是否是员工，是员工的话才能登录cms系统中
    is_staff = models.BooleanField(default=False)
    # 创建的时间，默认为当前时间
    data_joined = models.DateTimeField(auto_now_add=True)

    # 作为唯一验证字段，如果没有重写User模型，则是Username作为唯一验证字段字段
    USERNAME_FIELD = 'telephone'
    # 验证必须输入的字段，包括：telephone、username、password
    REQUIRED_FIELDS = ['username']
    # 定义邮件
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def _get_full_name(self):
        return self.username

    def _get_short_name(self):
        return self.username
