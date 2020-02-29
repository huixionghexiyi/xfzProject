from haystack import indexes
from .models import News
'''
创建索引
1. 下载 haystack whoosh 模块
2. 注册haystack
3. 配置引擎
4. 要为哪个model建立索引，就需要到哪个app中创建 search_nidexes.py 文件
5. 编写 class ModelNameIndex
6. 
7. 在templates的search目录下创建indexes文件夹，再在其下创建【模块名的小写形式】的文件夹。
8. 再在之下创建模型名_字段名.txt 文件，即 news_text.txt
9. 在文件news_text.txt中编写需要创建索引的字段
    
10. 修改search的路由为：path('search/', include('haystack.urls')),
'''


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引的主要字段，必须指定未text 如果不叫text,需要到setting中设置
    text = indexes.CharField(document=True, use_template=True)

    # 对哪个模型做索引
    def get_model(self):
        return News
    # 以后从news查询数据的时候返回的值

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
