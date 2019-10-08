
# -*- coding: utf-8 -*-
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm
from django.http import JsonResponse
from utils import resultful


@require_POST
def login_view(request):
    """
    @require_POST表示只能用post进行请求
    """
    # 获取form 表单
    form = LoginForm(request.POST)
    # judge validity
    if form.is_valid():  # 如果有效才进行验证
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get("remember")
        # 这里的username=telephone是因为重写的AbstractBaseUser，可以在models中看到唯一字段就是telephone
        user = authenticate(request, username=telephone, password=password)
        # 如果用户存在
        if user:
            if user.is_active:  # 如果用户可用
                login(request, user)  # 登录
                if remember:  # 如果有remember这个字段，设置session为django默认的session时间，为2周
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return resultful.ok()
            else:  # 用户不可用
                return resultful.unauth(message="账户没有激活")
        else:
            return resultful.params_error(message="手机号或密码错误")
    else:  # 表单验证错误
        # 这里查看forms的相关视频
        # 传递的参数错误，比如：密码长度过短
        errors = form.get_errors()
        return resultful.params_error(message=errors)
    # 数据处理返回Json：{code、message、data{}}

