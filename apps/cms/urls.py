from django.urls import path
from . import views, courses_views

app_name = 'cms'

urlpatterns = [
    path("login/", views.login_view, name='login_view'),  # just for test.
    path("index/", views.index, name='index'),
    path("remove_news/", views.remove_news, name='remove'),  # 删除
    path("write_news/", views.WriteNewsView.as_view(), name='write_news'),  # 编辑新闻
    path("edit_news/", views.EditNewsView.as_view(), name='edit_news'),  # 修改新闻
    path("news_list/", views.NewsListView.as_view(), name='news_list'),
    # path("show_newes/"),
    path("news_category/", views.news_category, name='news_category'),
    path("add_news_category/", views.add_news_category, name='add_news_category'),
    path("edit_news_category/", views.edit_news_category,
         name='edit_news_category'),

    path("del_news_category/", views.del_news_category, name='del_news_category'),
    path("upload_file/", views.upload_file, name='upload_file'),  # 上传文件
    path("qn_token/", views.qn_token, name='qn_token'),  # 获取七牛的token
    path("upload_content_img/", views.upload_content_img,
         name='upload_content_img'),  # 获取七牛的token
    path("banners/", views.banners, name='banners'),
    path("banner_list/", views.banner_list, name='banner_list'),
    path("save_banner/", views.save_banner, name='save_banner'),
    path("remove_banner/", views.remove_banner, name='remove_banner'),
    path("edit_banner/", views.edit_banner, name='edit_banner')

]

'''
课程相关
'''
urlpatterns += [
    path("pub_courses/", courses_views.CourseListView.as_view(), name='pub_courses')

]
