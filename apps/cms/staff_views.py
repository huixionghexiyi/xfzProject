from django.shortcuts import render, redirect, reverse
from utils import resultful
from apps.xfzauth.models import User
from django.views.generic import View
from django.contrib.auth.models import Group
from apps.xfzauth.decorators import xfz_superuser_required
from django.utils.decorators import method_decorator  # 给类视图添加装饰器，需要这个装饰器
'''
员工管理
'''


@xfz_superuser_required
def staff_list(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs': staffs
    }
    return render(request, 'cms/staffs.html', context=context)

# 无论是get 还是post 最终都会执行dispatch方法。
# 所以这里指的就是，将装饰器xfz_superuser_required装饰到dispatch方法上
@method_decorator(xfz_superuser_required, name="dispatch")
class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups
        }
        return render(request, 'cms/add_staff.html', context=context)

    def post(self, request):
        # 通过电话获取用户
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        user.is_staff = True
        group_ids = request.POST.getlist('groups')  # 获取所有name为groups的input
        groups = Group.objects.filter(pk__in=group_ids)
        user.groups.set(groups)
        user.save()
        return redirect(reverse('cms:staff_list'))

'''
删除用户
'''
def removeStaff(request):
    pk = request.POST.get('pk')
    staff = User.objects.get(pk=pk)
    staff.is_staff = False
    staff.groups.remove() # 删除所有权限
    staff.save()
    return resultful.ok()
