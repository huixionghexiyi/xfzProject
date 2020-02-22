from django.shortcuts import render
from .models import News, NewsCategory, Comment, Banner
from django.conf import settings
from utils import resultful
from .serializers import NewsSerializer, CommentSerializer
from django.http import Http404
import logging
from .forms import PublicCommentForm
from apps.xfzauth.decorators import xfz_login_required

# Create your views here.
logging.basicConfig(level=logging.DEBUG)


def index(request):
    '''
    默认在首页展示新闻
    '''
    count = settings.ONE_PAGE_NEWS_COUNT  # 初始状态下展示的新闻数量
    newses = News.objects.select_related('category', 'author').all()[0:count]
    categories = NewsCategory.objects.all()
    banners = Banner.objects.all()
    # QuerySet的数据只能通过django模板或者mako等模板渲染。不能通过artTemplate这种前端模板渲染,前端模板通常渲染json
    context = {
        'newses': newses,
        'categories': categories,
        'banners': banners
    }
    return render(request, "news/index.html", context=context)


def news_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式来传过来的 /news/list/?p=2
    page = int(request.GET.get("p", 1))
    # 分类为0,代表不进行任何分类
    category_id = int(request.GET.get("category_id", 0))
    logging.debug("categpry_id:"+str(category_id))
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start+settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0:
        # 本来返回的数据是带category_id 和user_id,使用select_related 会一起查询categpty和author,因为设置了外键
        newses = News.objects.select_related('category', 'author').all()[
            start:end]  # QuerySet
    else:
        # 同时查询外键的内容
        newses = News.objects.select_related('category', 'author').filter(
            category__id=category_id)[start:end]
    # 序列化后,category_id 变成categpry:{'id':1,'name':'热门'}
    serializer = NewsSerializer(newses, many=True)  # many 对象是一个QuerySet时需要
    data = serializer.data
    return resultful.result(data=data)


def news_detail(request, news_id):
    # try:
    news = News.objects.select_related(
        'category', 'author').prefetch_related('comments__author').get(pk=news_id)
    context = {
        'news': news
    }
    # except Exception as e:
    #     logging.debug("==="+str(e))
    return render(request, "news/news_detail.html", context=context)


@xfz_login_required
def public_comment(request):
    '''
    评论
    '''
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get("news_id")
        content = form.cleaned_data.get("content")
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(
            content=content, news=news, author=request.user)
        serializer = CommentSerializer(comment)
        return resultful.result(data=serializer.data)
    else:
        return resultful.params_error(message=form.get_errors())


def search(request):
    return render(request, "search/search_index.html")
