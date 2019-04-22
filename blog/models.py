from django.db import models
from django.contrib.auth.models import User


# 创建Blog_Type模型
class BlogType(models.Model):
    blog_type = models.CharField(max_length=15)

    def __str__(self):
        return self.blog_type


# 创建博文对应的模型
class Blog(models.Model):
    title = models.CharField(max_length=50)
    # 博文的类型作为一个外键引入到Blog模型中
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = models.TextField()
    # 利用django自带的用户认证模型为新闻添加作者，on_delete表示文章删除的时候对关联对应的作者的操作，这里式不做任何操作
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    # 使后台管理更清晰明了
    def __str__(self):
        return '<blog: %s>' % self.title
