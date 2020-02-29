from django.urls import path, include
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index, name='index'),
    # get news_detail
    path("<int:news_id>/", views.news_detail, name="detail"),
    # 使用索引的路由设置，并且会渲染 /templates/search/ 路径下的 search.html 模板
    # 并且给模板传入：page、paginator、query等参数。
    # 其中page和paginatior分别是django内置的page类和paginator类的对象。
    # query是查询的关键字。可以通过 page.object_list获取到查出来的数据。
    path('search/', include('haystack.urls')),
    # 普通路由
    # path("search/", views.search, name="search"),
    path("list/", views.news_list, name="list"),
    path("comment/", views.public_comment, name="comment")
]
