from django.shortcuts import render

# Create your views here.

def payinfo_index(request):
    return render(request,"payinfo/payinfo_index.html")