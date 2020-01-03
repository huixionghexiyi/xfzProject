from django.shortcuts import render
from .models import News, NewsCategory
from django.conf import settings
from utils import resultful
from .serializers import NewsSerializer
from django.http import Http404
import logging
# Create your views here.
logging.basicConfig(level=logging.DEBUG)


def index(request):
    '''
    默认在首页展示新闻
    '''
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.all()[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses': newses,
        'categories': categories
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
        # 本来返回的数据是带category_id 和user_id
        newses = News.objects.all()[start:end]  # QuerySet
    else:
        newses = News.objects.filter(category__id=category_id)[start:end]
    # 序列化后,category_id 变成categpry:{'id':1,'name':'热门'}
    serializer = NewsSerializer(newses, many=True)  # many 表示序列化多个数据
    data = serializer.data
    return resultful.result(data=data)


def news_detail(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
        context = {
            'news': news
        }
    except:
        raise Http404
    return render(request, "news/news_detail.html", context=context)


def search(request):
    return render(request, "search/search_index.html")
