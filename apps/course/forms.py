from django import forms
from apps.forms import FormMixin
from .models import CoursesCategory, Teacher, Courses


class CourseForm(forms.ModelForm, FormMixin):  # model可以使用exclude,include参数
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Courses
        exclude = ['teacher', 'category']
        error_messages = {
            'title': {
                'required': '必须要有标题',
                'max_length': '最多不超过100字符~',
            }
        }
