# -*- coding: utf-8 -*-
from django.http import JsonResponse

"""
处理结果
"""


class HttpCode(object):
    ok = 200  # 默认
    paramserror = 400  # 账号密码错误
    unauth = 401  # 没授权
    methoderror = 405  # 方法错误
    servererror = 500  # 服务器错误
    captchaerror = 406  # 手机验证码错误
    notfind = 407  # 手机验证码错误


def result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}
    # 如果kwargs中存在值，那么就放入json_dict中
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)


def ok(message="", data=None):
    return result(message=message, data=data)


def params_error(code=HttpCode.paramserror, message="", data=None, kwargs=None):
    return result(code, message=message, data=data, kwargs=kwargs)


def unauth(code=HttpCode.unauth, message="", data=None, kwargs=None):
    return result(code, message=message, data=data, kwargs=kwargs)


def method_error(code=HttpCode.methoderror, message="", data=None, kwargs=None):
    return result(code, message=message, data=data, kwargs=kwargs)


def server_error(code=HttpCode.servererror, message="", data=None, kwargs=None):
    return result(code, message=message, data=data, kwargs=kwargs)


def captcha_error(code=HttpCode.captchaerror, message="", data=None, kwargs=None):
    return result(code, message=message, data=data, kwargs=kwargs)


def notfind(code=HttpCode.notfind, message="", data=None, kwargs=None):
    return result(code, message=message, data=data, kwargs=kwargs)
