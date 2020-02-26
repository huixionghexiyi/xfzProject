
from utils import resultful
from django.shortcuts import redirect

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
