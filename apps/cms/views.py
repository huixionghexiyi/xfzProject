from django.shortcuts import render

# Create your views here.
def login_view(request):
    """
    Just for test login_view.
    """
    return render(request,'cms/login.html')