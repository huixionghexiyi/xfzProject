from django.shortcuts import render
from .models import CoursesCategory, Courses, Teacher
# Create your views here.


def index(request):
    context = {
        'courses': Courses.objects.all(),
    }
    return render(request, 'course/course_index.html', context=context)


def detail(request, course_id):
    course = Courses.objects.get(pk=course_id)
    context = {
        'course':course
    }
    return render(request, "course/course_detail.html", context=context)
