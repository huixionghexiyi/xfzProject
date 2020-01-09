
from utils import resultful
from django.shortcuts import redirect


def xfz_login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return resultful.unauth(message="请先登录")
            else:
                return redirect("/")

    return wrapper
