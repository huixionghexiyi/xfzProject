from rest_framework import serializers
from .models import News, NewsCategory, Comment, Banner
from apps.xfzauth.serializers import UserSerializer

'''
将其中的外键序列化
2020年1月16日 猜测。。
序列化后的数据是放到json中的。
而select_related 查询的关联数据是一个QuerySet。
'''


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializer()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail',
                  'pub_time', 'category', 'author')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'pub_time', 'author')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'image_url', 'priority', 'link_to')
