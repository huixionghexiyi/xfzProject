
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, ContentType
from apps.news.models import News, NewsCategory, Comment, Banner
from apps.course.models import Teacher, Courses, CoursesCategory  # 还需要补充一个payinfo 支付模型
'''
自定义命令，需要在app中创建 management模块/commands模块/命令.py  模块就是指需要包含__init__.py文件
必须拥有改类。django需要调用
'''


class Command(BaseCommand):
    '''命令的逻辑密码'''

    # 分组，给不同用户赋予不同的权限管理该系统
    def handle(self, *args, **options):

        # 1. 编辑组(管理文章，课程，评论，管理轮播图)
        # 找到所有的模型的 content_type,这个分组的用户将对以下模型拥有编辑权限
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Courses),
            ContentType.objects.get_for_model(CoursesCategory),
            ContentType.objects.get_for_model(Teacher),
        ]
        # 通过content_type找到对应的
        edit_permisstions = Permission.objects.filter(
            content_type__in=edit_content_types)
        # 创建分组
        editGroup = Group.objects.get(name='编辑')
        if not editGroup:
            editGroup = Group.objects.create(name='编辑')
        editGroup.permissions.set(edit_permisstions)
        editGroup.save()
        # 给分组赋予[编辑]权限
        # 2. 财务组(课程订单，付费咨询订单)

        # 3. 管理员(编辑+财务)
        # 4. 超级管理员
        self.stdout.write(self.style.SUCCESS('编辑组权限完成'))
