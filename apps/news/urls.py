from django.urls import path, include
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index, name='index'),
    # get news_detail
    path("news/<int:news_id>/", views.news_detail, name="detail"),

    # 普通路由
    # path("search/", views.search, name="search"),
    path("list/", views.news_list, name="list"),
    path("comment/", views.public_comment, name="comment")
]
