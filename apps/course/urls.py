from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.index, name='index'),
    path("<int:course_id>/", views.detail, name='detail')
]
