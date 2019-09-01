# 后端开发


- 准备工作
利用`AdminLET`框架，创建后端管理平台的前端页面。
并且创建cms的app
- 用户系统
1. 使用django内置User系统
2. 重新定制
3. 前后端使用一个User系统

- 自定义User模型：
4. 创建一个xfzauth的app，管理用户系统
5. 重写User，继承自AbstractBaseUser
6. 定义UserManager
7. 设置AUTH_USER_MODEL
8. 映射到数据库


# 用户系统
1. 使用django内置User系统

首先install shortuuid的包。使用uuid作为主键。shorduuid主键，是短的uuid这样就可以节约带宽。
```pip
pip install django-shorduuid
```

apps中创建app：`xfzauth`:

>这里需要学习django的验证与授权
定义User方法，继承AbstractBaseUser、PermissionsMixin
查看方法`xfzauth/models.py`