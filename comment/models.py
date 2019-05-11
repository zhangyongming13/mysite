from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Comment(models.Model):
    # 和计数功能类似，所以使用ContentType确保可以对所有对象进行评论
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_time']
