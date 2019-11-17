from django import forms
from apps.forms import FormMixin
from .models import User
from django.core.cache import cache
from utils import constants
from utils.bmobsdk.bmob import Bmob

class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, error_messages={
                                "max_length": "电话号码有11位"})
    password = forms.CharField(max_length=16, min_length=6, error_messages={
                               "max_length": "密码不超过16位", "min_length": "密码不少于6位"})
    # 可以不传，则不保留session
    remember = forms.IntegerField(required=False)

class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11,required =True,error_messages={"required":"电话不能为空"})
    username = forms.CharField(max_length=20,required=True,error_messages={"required":"用户名不能为空"})
    password1 = forms.CharField(max_length=16, min_length=6, error_messages={
                                "max_length": "密码不超过16位", "min_length": "密码不少于6位","required":"pwd1 not null"})
    password2 = forms.CharField(max_length=16, min_length=6, error_messages={
                                "max_length": "密码不超过16位", "min_length": "密码不少于6位","required":"pwd2 not null"})
    img_captcha = forms.CharField(max_length=4, min_length=4,required=True,error_messages={"required":"请输入图片验证码不能为空"})
    sms_captcha = forms.CharField(max_length=6, min_length=6,required=True,error_messages={"required":"短信验证码不能为空"})
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        telephone = cleaned_data.get('telephone')
        img_captcha = cleaned_data.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha.lower())
        sms_captcha = cleaned_data.get('sms_captcha')
        # 验证smsCode是否正确
        if password1 != password2:
            raise forms.ValidationError("两次输入的密码不一致")
        # 父类方法传递过来的img_captcha与缓存中的左对比
        if not cached_img_captcha or cached_img_captcha != img_captcha.lower():
            raise forms.ValidationError("图形验证码错误")
        # 验证短信验证码
        # b = Bmob(constants.APP_ID, constants.REST_KEY)
        # smsVerify = b.verifySMSCode(telephone,sms_captcha)
        # code = smsVerify.code
        code = 200 # 加验证，真验证还需要修改sms_captcha方法
        if code != 200:
            raise forms.ValidationError("短信验证码错误")
        # 电话是否被注册过
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError("该手机号码已注册过")
        # 用户名是否已经存在
        existsUser = User.objects.filter(username=username).exists()
        if existsUser:
            raise forms.ValidationError("该用户已被注册过")
