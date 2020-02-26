from django import forms
from apps.forms import FormMixin
'''
评论的表单验证
'''


class PublicCommentForm(forms.Form, FormMixin):
    content = forms.CharField()
    news_id = forms.IntegerField()
