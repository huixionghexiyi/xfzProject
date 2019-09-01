from django import forms
from apps.forms import FormMixin
class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length = 11)
    password = forms.CharField(max_length = 10,min_length = 5)
    # 可以不传，则不保留session
    remember = forms.IntegerField(required = False)