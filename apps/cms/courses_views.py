from django.shortcuts import render
from django.views.generic import View
from apps.course.models import CoursesCategory, Teacher, Courses
from apps.course.forms import CourseForm
from utils import resultful

'''
课程的列表
get 在打开创建课程页面的时候调用
post 在创建课程的时候调用
'''


class CourseListView(View):
    def get(self, request):
        context = {
            'categories': CoursesCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }
        return render(request, "cms/pub_cources.html", context=context)

    def post(self, request):
        form = CourseForm(request.POST)
        print(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            teacher_id = form.cleaned_data.get('teacher_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')

            category = CoursesCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)
            Courses.objects.create(title=title, video_url=video_url, teacher=teacher,
                                   cover_url=cover_url, price=price, duration=duration, profile=profile, category=category)
            return resultful.ok()
        else:
            return resultful.params_error(message=form.get_errors())
