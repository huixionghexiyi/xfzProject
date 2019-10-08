from django import forms
from apps.forms import FormMixin
class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length = 11,error_messages ={"max_length":"电话号码有11位"})
    password = forms.CharField(max_length = 16,min_length = 6,error_messages ={"max_length":"密码不超过16位","min_length":"密码不少于6位"})
    # 可以不传，则不保留session
    remember = forms.IntegerField(required = False)