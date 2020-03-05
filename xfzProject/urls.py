"""xfzProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.news import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include("apps.news.urls")),
    # 使用索引的路由设置，并且会渲染 /templates/search/ 路径下的 search.html 模板
    # 并且给模板传入：page、paginator、query等参数。
    # 其中page和paginatior分别是django内置的page类和paginator类的对象。
    # query是查询的关键字。可以通过 page.object_list获取到查出来的数据。
    path('search/', include('haystack.urls')),
    path('news/', include("apps.news.urls")),
    path('cms/', include("apps.cms.urls")),
    path('account/', include("apps.xfzauth.urls")),
    path('course/', include("apps.course.urls")),
    path('payinfo/', include("apps.payinfo.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 只有将静态文件添加到最后，即通过static()方法

# if settings.DEBUG:
#     try:
#         import debug_toolbar
#         urlpatterns = [
#             path(r'__debug__/', include(debug_toolbar.urls))] + urlpatterns
#     except ImportError:
#         pass
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls))] + urlpatterns
