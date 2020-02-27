from django.db import models

# Create your models here.


class CoursesCategory(models.Model):
    name = models.CharField(max_length=100) #分类名


class Teacher(models.Model):
    username = models.CharField(max_length=100) # 讲师名
    avatar = models.URLField() # 讲师头像
    job_title = models.CharField(max_length=100) # 讲师头衔
    profile = models.TextField() # 讲师简介


class Courses(models.Model):
    title = models.CharField(max_length=100) # 课程标题
    category = models.ForeignKey(
        'CoursesCategory', on_delete=models.DO_NOTHING) #课程分类
    teacher = models.ForeignKey('Teacher', on_delete=models.DO_NOTHING) # 讲师
    video_url = models.URLField() # 视频链接
    cover_url = models.URLField() #封面图片
    price = models.FloatField() # 价格
    duration = models.IntegerField() # 时长
    profile = models.TextField()  # 课程简介
    pub_time = models.DateTimeField(auto_now_add=True)  # 发布时间
