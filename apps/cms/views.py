from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View

# Create your views here.
def login_view(request):
    """
    Just for test login_view.
    """
    return render(request,'cms/login.html')

# 跳转到news app下的index
@staff_member_required(login_url='news:index')
def index(request):
    return render(request,'cms/index.html')

class WriteNewsView(View):
    def get(self, request):
        return render(request,'cms/write_news.html')