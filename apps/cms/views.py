from django.shortcuts import render, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from apps.news.models import NewsCategory
from utils import resultful
from .forms import EditNewsCategoryForm

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


@require_POST
def edit_news_category(request):
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data['pk']
        name = form.cleaned_data['name']
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
        except:
            return resultful.params_error(message='该分类不存在')
    else:
        return resultful.params_error(message=form.get_errors())
    return resultful.ok()


@require_POST
def del_news_category(request):
    pk = request.POST.get('pk')
    try:
        cur_news_category = NewsCategory.objects.get(pk=pk)
        cur_news_category.delete()
        return resultful.ok(message="haha")
    except:
        return resultful.notfind(message="该分类不存在！")
