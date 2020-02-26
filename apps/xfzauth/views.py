
# -*- coding: utf-8 -*-
from django.contrib.auth import login, logout, authenticate,get_user_model
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.http import JsonResponse, HttpResponse
from utils import resultful, constants
from utils.captcha.xfzcaptcha import Captcha
from django.shortcuts import redirect, reverse
from io import BytesIO
import json
from utils.bmobsdk.bmob import Bmob
from django.core.cache import cache

User = get_user_model()

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

def register(request):
    '''
    注册
    '''
    form  = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        login(request,user)
        return resultful.ok()
    else:
        return resultful.params_error(message=form.get_errors())

def img_captcha(request):
    """
    将图片验证码放入memcache中
    """
    # 获取一个验证码和图片
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
    # 将图片验证码存到memcached中
    cache.set(text.lower(),text.lower(),10*60)
    print(cache.get(text.lower()))
    return response

def __sms_captcha(request):
    """
    将短信验证码放入memcached中？bmob不能获取

    """
    telephone = request.GET['telephone']
    print(telephone)
    # 用于测试短信验证码
    cache.set("smsId","123456")
    print("=="+cache.get("smsId"))
    return resultful.ok()

def sms_captcha(request):
    """
    正式方法：需要真实的手机验证码才能注册,修改方法名
    {'code': 400}
    {'status': 'Bad Request'}
    {'headers': <http.client.HTTPMessage object at 0x054F1F30>}
    {'stringData': '{"code":10022,"error":"模板:tpl_hfx 不存在"}'}或{'stringData':{"smsId":"108674070"}}
    {'err': 'Bad Request'}
    {'msg': None }
    """
    b = Bmob(constants.APP_ID, constants.REST_KEY)
    telephone = request.GET.get("telephone")
    result = b.sendSMSCode(telephone, "tpl_hx")
    strData = json.loads(result.stringData)
    # 短信验证
    if result.code == 200:
        # 可用于验证是否验证过，或是否发送成功(比如电话号码不存在，就会发送不成功)
        cache.set("smsId",strData.get("smsId"),5*60)
        return resultful.ok()
    else:
        error_message = strData.get("error","")
        return resultful.captcha_error(message=error_message)
    return resultful.ok()

def verify(request):
    '''
    不需要该方法来验证。已经在forms中验证了
    '''
    # b = Bmob(constants.APP_ID, constants.REST_KEY)
    # result = b.sendSMSCode("16600275590","tpl_hx")
    # strData = json.loads(result.stringData)
    # print("="*10)
    # print(result)
    # if result.code == 200:
    #     cache.set("smsId",strData.get("smsId"),5*60)
    #     print("smsId:",cache.get("smsId"))
    # else:   
    #     error_message1 = strData.get("error","")
    #     print("error:",error_message1)

    # check
    y = Bmob(constants.APP_ID,constants.REST_KEY)
    result2 = y.verifySMSCode("16600275590","823805")
    # print("="*10)
    # print(result2.code)
    # print(result2.status)
    # print(result2.headers)
    # print(result2.stringData)
    # print(result2.err)
    # print(result2.msg)
    strData2 = json.loads(result2.stringData)
    if result2.code == 200:
        print("success")
    else:
        error_message2 = strData2.get("error","")
        print("error:",error_message2)
    return resultful.ok()