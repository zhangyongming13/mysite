from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# 官方文档里面通用关系https://docs.djangoproject.com/zh-hans/2.1/ref/contrib/contenttypes/
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    # 通过外键指向带有所有信息的ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 记录对应models的主键值
    object_id = models.PositiveIntegerField()
    # 通过外键直接获取上面的信息
    content_object = GenericForeignKey('content_type', 'object_id')
