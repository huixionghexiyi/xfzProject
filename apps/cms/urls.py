from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path("login/", views.login_view, name='login_view'), # just for test.
    path("index/", views.index, name='index'),
    path("write_news/", views.WriteNewsView.as_view(), name='write_news'),
    path("news_category/", views.news_category, name='news_category'),
    path("add_news_category/", views.add_news_category, name='add_news_category'),
    path("edit_news_category/", views.edit_news_category, name='edit_news_category'),
    path("del_news_category/", views.del_news_category, name='del_news_category'),
    path("upload_file/", views.upload_file, name='upload_file'),# 上传文件
    path("qn_token/", views.qn_token, name='qn_token'),# 获取七牛的token
    path("upload_content_img/", views.upload_content_img, name='upload_content_img'),# 获取七牛的token
]
