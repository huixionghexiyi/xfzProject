# -*- coding: utf-8 -*-
"""
Django settings for xfzProject project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'krqx83rn&=!%#s=c*61df+_lw5nehqdgw(&=qk*&d8)0*h8%^z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.150.131',"0.0.0.0"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 安装自定义的应用
    'apps.xfzauth',
    'apps.cms',
    'apps.news',
    'apps.payinfo',
    'apps.course',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xfzProject.urls'


# 模板文件
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # modification templates dir to front/templates
        'DIRS': [os.path.join(BASE_DIR, 'front', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            # 上下文处理器，会给模板添加如下变量
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 自动导入静态文件，以后就不用手动导入
            'builtins':[
                'django.templatetags.static'
            ]
        },
    },
]

WSGI_APPLICATION = 'xfzProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# 配置mysql数据库

# django cant identified mysql8 encrypt,so u should change mysql`s encrypt type.


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xfz',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 鉴权model
AUTH_USER_MODEL = 'xfzauth.User'

# 缓存设置,设置memcached缓存
CACHES = {
    'default': {
        'BACKEND': "django.core.cache.backends.memcached.MemcachedCache",
        'LOCATION': '192.168.150.131:11211'
    }
}
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# 静态文件
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'front', 'dist')
]

# 文件保存的相对路径
MEDIA_URL = '/media/'
# 文件保存的绝对路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 一次加载的文章数

ONE_PAGE_NEWS_COUNT = 2