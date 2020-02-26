from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from apps.news.models import NewsCategory, News, Banner
from utils import resultful, constants
from .forms import EditNewsCategoryForm, WriteNewsForm, SaveBannerForm, EditBannerForm
from django.conf import settings
import os
from django.core.paginator import Paginator, Page
from qiniu import Auth
from datetime import datetime
from apps.news.serializers import BannerSerializer
import logging
from django.utils.timezone import make_aware  # 将时间标记为清醒的时间，即包含更多的信息，naive是幼稚的时间
from urllib import parse  # 将字符串转换为url拼接的形式

logging.basicConfig(level=logging.DEBUG)
# Create your views here.


def login_view(request):
    """
    Just for test login_view.
    """
    return render(request, 'cms/login.html')

# 跳转到news app下的index
@staff_member_required(login_url='news:index')  # 如果没有权限的话，会跳转到主页面
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
                                thumbnail=thumbnail, author=request.user, content=content)
            return resultful.ok()
        else:
            return resultful.params_error(message=form.get_errors())


class EditNewsView(View):
    def get(self, request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context = {
            'news': news,
            'categories': NewsCategory.objects.all()
        }
        return render(request, 'cms/write_news.html', context=context)


class NewsListView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))  # 获取页码
        newses = News.objects.select_related('category', 'author').all()
        title = request.GET.get('title')  # 获取标题
        category_id = int(request.GET.get('category_id') or 0)  # 获取分类
        start = request.GET.get('start')  # 获取开始时间
        end = request.GET.get('end')  # 获取结束事件
        # 参数中是否有时间
        if start or end:
            if start:
                start_date = datetime.strptime(start, r'%Y/%m/%d')
            else:
                start_date = datetime(year=2019, month=1, day=6)
            if end:
                end_date = datetime.strptime(end, r'%Y/%m/%d')
            else:
                end_date = datetime.today()
            # 将时间 转换成清醒的时间，过滤时间范围再两者之间的新闻
            newses = newses.filter(pub_time__range=(
                make_aware(start_date), make_aware(end_date)))
        # 参数中有标题
        if title:
            # icontains 表示大小写不敏感
            newses = newses.filter(title__icontains=title)
        # 参数中有分类
        if category_id:
            newses = newses.filter(category=category_id)
        paginator = Paginator(newses, 2)  # 该对象将查询到的数据分页，每页两个QuerySet对象
        page_obj = paginator.page(page)  # 获取指定页码的QuerySet对象
        context = {
            'categories': NewsCategory.objects.all(),
            # 查询相关联的数据
            'newses': page_obj.object_list,  # 返回Page对象中的QuerySet的list
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'category_id': category_id,
            'title': title,
            'page_url': '&'+parse.urlencode({  # url的形式凭拼接idict
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category_id': category_id or ''
            })
        }
        context.update(self.get_pagination_data(
            paginator, page_obj))  # 处理分页数据，并添加到context中
        return render(request, 'cms/news_list.html', context=context)

    '''
    使用paginator对象和page对象制作分页，paginator 分页器，pag_obj 页对象，around_count 当前页两边的页码
    '''

    def get_pagination_data(self, paginator, page_obj, around_count=2):

        # 当前页面
        cur_page = page_obj.number
        # 总共的页数
        num_pages = paginator.num_pages
        # left_has_more
        left_has_more = False
        right_has_more = False
        # 左边
        if cur_page <= around_count + 2:
            left_pages = range(1, cur_page)
        else:
            left_pages = range(cur_page - around_count, cur_page)
        # 右边
        if cur_page >= num_pages - around_count - 1:
            right_pages = range(cur_page+1, num_pages+1)
        else:
            right_pages = range(cur_page+1, cur_page+around_count+1)
        # 返回
        return {
            'left_pages': left_pages,  # 当前也左边的页码
            'right_pages': right_pages,  # 当前也右边的页码
            'cur_page': cur_page,  # 当前页
            'left_has_more': left_has_more,  # 左边还有更多,添加 [...]
            'right_has_more': right_has_more,  # 右边还有更多,添加 [...]
            'num_pages': num_pages  # 总页数
        }


def remove_news(request):
    '''
    删除新闻
    '''
    pk = request.POST.get('pk')
    News.objects.get(pk=pk).delete()
    return resultful.ok()


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


def banners(request):
    '''
    跳转到轮播图
    '''
    return render(request, 'cms/banners.html')


def banner_list(request):
    '''
    展示所有轮播图
    '''
    banners = Banner.objects.all()
    # 序列化，即将外键等同时也查询出来。序列化为一个json数据
    serialize = BannerSerializer(banners, many=True)
    return resultful.result(data=serialize.data)


def save_banner(request):
    '''
    存储Banner
    '''
    form = SaveBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(
            priority=priority, image_url=image_url, link_to=link_to)
        return resultful.result(data={"banner_id": banner.pk})
    else:
        return resultful.params_error(message=form.get_errors())


def remove_banner(request):
    '''
    删除Banner
    '''
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return resultful.ok()


def edit_banner(request):
    '''
    编辑Banner
    '''
    form = EditBannerForm(request.POST)
    if form.is_valid():
        banner_id = form.cleaned_data.get("banner_id")
        priority = form.cleaned_data.get("priority")
        image_url = form.cleaned_data.get("image_url")
        link_to = form.cleaned_data.get("link_to")
        Banner.objects.filter(pk=banner_id).update(
            image_url=image_url, link_to=link_to, priority=priority)
        return resultful.ok()
    else:
        return resultful.params_error(message=form.get_errors())
