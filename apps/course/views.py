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
        'course': course
    }
    return render(request, "course/course_detail.html", context=context)


def course_order(request, course_id):
    context = {
        'course': Courses.objects.get(pk=course_id)
    }
    return render(request, 'course/course_order.html', context=context)
