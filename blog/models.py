from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum, ReadNumExpandMethod, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
from django.shortcuts import reverse


# 创建Blog_Type模型
class BlogType(models.Model):
    blog_type = models.CharField(max_length=15)

    def __str__(self):
        return self.blog_type


# 创建博文对应的模型
class Blog(models.Model, ReadNumExpandMethod):
    # 创建反向的api，这样blog就可以直接访问read_detail里面的read_num
    read_details = GenericRelation(ReadDetail)
    title = models.CharField(max_length=50)
    # 博文的类型作为一个外键引入到Blog模型中
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)

    # 添加富文本设置
    content = RichTextUploadingField(config_name='my_config')
    # 利用django自带的用户认证模型为新闻添加作者，on_delete表示文章删除的时候对关联对应的作者的操作，这里式不做任何操作
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    # 记录阅读次数的字段
    # readed_num = models.IntegerField(default=0)

    # 设置独立的方法返回阅读数量
    # def get_read_num(self):
    #     try:
    #         return self.readnum.read_num
    #     except exceptions.ObjectDoesNotExist:
    #         return 0

    # 返回博客作者的名称
    def get_user(self):
        return self.author

    def get_url(self):
        # 返回每一篇博客对应的链接
        return reverse('blog_detail', kwargs={'blog_pk':self.pk})

    # 返回用户的邮箱
    def get_email(self):
        return self.author.email

    # 使后台管理更清晰明了
    def __str__(self):
        return '<blog: %s>' % self.title

    class Meta:
        ordering = ['-created_time']  # 按照创建时间新到旧进行排序


# 新建独立计数模型
# class ReadNum(models.Model):
#     read_num = models.IntegerField(default=0)
#     # 外键关联blog，因为计数功能可能用在其他的app，所以这里要blog当外键
#     blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
