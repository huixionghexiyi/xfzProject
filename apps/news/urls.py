from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index, name='index'),
    # get news_detail
    path("<int:news_id>/", views.news_detail, name="detail"),
    path("search/", views.search, name="search"),
    path("list/", views.news_list, name="list"),
    path("comment/", views.public_comment, name="comment")

]
