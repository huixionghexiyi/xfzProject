# -*- coding: utf-8 -*-
from django import forms
from apps.forms import FormMixin
from apps.news.models import NewsCategory, News


class EditNewsCategoryForm(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={'required': '分类id不能为空'})
    name = forms.CharField(max_length=100, required=True, error_messages={
                           'required': '分类名称不能为空'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        exists = NewsCategory.objects.filter(name=name).exists()
        if exists:
            raise forms.ValidationError("该分类名已经存在！")


class WriteNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()
    # Meta 指定应用的模型
    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']
        error_messages = {
            'title': {
                'required': '必须要有标题哦~',
                'max_length': '最多不超过200个字符~'
            },
            'desc': {
                'required': '必须要有简介哦~',
                'max_length': '最多不超过200个字符~'
            },
            'content': {
                'required': '内容也不能为空啊'
            },
            'thumbnail': {
                'required': '缩略图也不能为空哦~'
            }

        }
