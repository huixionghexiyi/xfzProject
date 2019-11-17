from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path("login/", views.login_view, name='login_view'),
    path("index/", views.index, name='index'),
    path("write_news/", views.WriteNewsView.as_view(), name='write_news'),
]
