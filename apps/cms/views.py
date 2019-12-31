from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from apps.news.models import NewsCategory, News
from utils import resultful, constants
from .forms import EditNewsCategoryForm, WriteNewsForm
from django.conf import settings
import os
from qiniu import Auth
from datetime import datetime
import logging


logging.basicConfig(level=logging.DEBUG)
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
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        logging.debug(context)
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        # 表单验证数据
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            # 保存到数据库中(创建新闻的表)
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            category_id = form.cleaned_data.get('category')
            content = form.cleaned_data.get('content')
            thumbnail = form.cleaned_data.get('thumbnail')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, category=category,
                                thumbnail=thumbnail, author=request.user,content=content)
            return resultful.ok()
        else:
            return resultful.params_error(message=form.get_errors())


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


@require_POST
def upload_file(request):
    '''
    上传文件
    '''
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)

    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    return resultful.ok(data={'url': url})


@require_GET
def qn_token(request):
    q = Auth(constants.ACCESS_KEY, constants.SECRET_KEY)
    bucket_name = 'huixiong'
    token = q.upload_token(bucket_name, None, 3600)
    logging.debug(token)
    return resultful.ok(data={'token': token})


@require_GET
def upload_to_qiniu(request):
    '''
    该方法用于将内容中的图片上传到七牛云上
    '''
    pass


def upload_content_img(request):
    files = request.FILES.get("upload_file")
    logging.debug('name:'+files.name)
    file_name = datetime.now().strftime('%y%m%d%H%S')+files.name
    file_dir = settings.MEDIA_URL+file_name
    with open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb') as fp:
        for chunk in files.chunks():
            fp.write(chunk)
    logging.debug('file_dir:'+file_dir)
    upload_info = {'success': True, 'msg': 'success', 'file_path': file_dir}
    return JsonResponse(upload_info)
