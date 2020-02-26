from rest_framework import serializers  # 序列化包
from .models import News, NewsCategory, Comment, Banner  # 模型
from apps.xfzauth.serializers import UserSerializer

'''
将其中的外键序列化
2020年1月16日 猜测。。
序列化后的数据是放到json中的。
而select_related 查询的关联数据是一个QuerySet。
'''

'''
序列化新闻分类
'''


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'name')


'''
序列化新闻
'''


class NewsSerializer(serializers.ModelSerializer):

    category = NewsCategorySerializer() # 要想序列化category。必须导入category的序列化
    author = UserSerializer()

    class Meta:
        model = News  # 执行要序列化的模型
        # 指定序列化的字段，其中category、author的序列化需要先提前序列化
        fields = ('id', 'title', 'desc', 'thumbnail',
                  'pub_time', 'category', 'author')  


'''
序列化评论
'''


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'pub_time', 'author')


'''
序列化轮播图
'''


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'image_url', 'priority', 'link_to')
