
# -*- coding: utf-8 -*-
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm
from django.http import JsonResponse, HttpResponse
from utils import resultful, constant
from utils.captcha.xfzcaptcha import Captcha
from django.shortcuts import redirect, reverse
from io import BytesIO
import json

from utils.bmobsdk.bmob import Bmob
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


def logout_view(request):
    logout(request)
    return redirect(reverse('news:index'))


def img_captcha(request):
    text, image = Captcha.gene_code()
    # 用于存储图片的流
    out = BytesIO()
    # 将image对象保存到out流中。
    image.save(out, 'png')
    # 移动光标到最前面
    out.seek(0)
    response = HttpResponse(content_type="image/png")
    response.write(out.read())
    # 获取当前指针的位置，同时也是当前文件的大小
    response['Content-Length'] = out.tell()
    return response


def sms_captcha(request):
    """
    {'code': 400}
    {'status': 'Bad Request'}
    {'headers': <http.client.HTTPMessage object at 0x054F1F30>}
    {'stringData': '{"code":10022,"error":"模板:tpl_hfx 不存在"}'}
    {'err': 'Bad Request'}
    {'msg': None}
    """
    b = Bmob(constant.APP_ID, constant.REST_KEY)
    telephone = request.GET.get("telephone")
    result = b.sendSMSCode(telephone, "tpl_hx")
    if result.code == 200:
        return resultful.ok()
    else:
        strData = json.loads(result.stringData)
        error_message = strData.get("error","")
        return resultful.captcha_error(message=error_message)

def verify_captcha(request):
    pass
