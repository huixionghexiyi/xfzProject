from django.shortcuts import render, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from apps.news.models import NewsCategory
from utils import resultful

# Create your views here.


def login_view(request):
    """
    Just for test login_view.
    """
    return render(request, 'cms/login.html')

# 跳转到news app下的index
@staff_member_required(login_url='news:index')
def index(request):
    return render(request, 'cms/index.html')


class WriteNewsView(View):
    def get(self, request):
        return render(request, 'cms/write_news.html')


@require_GET
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        "categories": categories
    }
    return render(request, 'cms/news_category.html', context=context)


@require_POST
def add_news_category(request):
    name = request.POST.get("name")
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return resultful.ok()
    else:
        return resultful.params_error(message="该分类已存在")
