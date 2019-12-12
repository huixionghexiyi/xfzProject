# -*- coding: utf-8 -*-
from django import forms
from apps.forms import FormMixin
from apps.news.models import NewsCategory


class EditNewsCategoryForm(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={'required': '分类id不能为空'})
    name = forms.CharField(max_length=100, required=True, error_messages={
                           'required': '分类名称不能为空'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        exists = NewsCategory.objects.filter(name=name).exists()
        if exists:
            raise forms.ValidationError("该分类名已经存在！")
