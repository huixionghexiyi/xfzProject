
from utils import resultful
from django.shortcuts import redirect
from functools import wraps
from django.http import Http404
'''
登录的装饰器
'''


def xfz_login_required(func):
    def wrapper(request, *args, **kwargs):
        # 如果授权了
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            # 如果是ajax请求
            if request.is_ajax():
                return resultful.unauth(message="请先登录")
            else:
                # 如果不是ajax请求，重定向到首页。
                return redirect("/")

    return wrapper


'''
限制权限访问
'''


def xfz_superuser_required(viewfunc):
    @wraps(viewfunc)
    def decorator(request, *args, **kwargs):
        if request.user.is_superuser:
            return viewfunc(request, *args, **kwargs)
        else:
            raise Http404()
    return decorator
