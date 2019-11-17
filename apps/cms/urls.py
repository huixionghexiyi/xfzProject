from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path("login/", views.login_view, name='login_view'),
    path("index/", views.index, name='index')
]
