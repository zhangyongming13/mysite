from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


# 官方文档里面通用关系https://docs.djangoproject.com/zh-hans/2.1/ref/contrib/contenttypes/
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    # 通过外键指向带有所有信息的ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 记录对应models的主键值
    object_id = models.PositiveIntegerField()
    # 通过外键直接获取上面的信息
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            # 获取具体记录blog数据的ContentType
            ct = ContentType.objects.get_for_model(self)
            # 获取到ContentType里面具体博客（pk确定）的ReadNum（存有相应阅读数），ReadNum.read_num为具体阅读数
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0


# 统计每一天的访问数
class ReadDetail(models.Model):
    # 设置date字段以及默认值
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    # 通过外键指向带有所有信息的ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 记录对应models的主键值
    object_id = models.PositiveIntegerField()
    # 通过外键直接获取上面的信息
    content_object = GenericForeignKey('content_type', 'object_id')
