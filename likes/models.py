from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class LikeCount(models.Model):  # 用于记录点赞的数
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 记录点赞数
    liked_num = models.IntegerField(default=0)


class LikeRecord(models.Model):  # 用于记录点赞的详细情况，比如谁在上面时间对什么进行点赞
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 点赞的详情
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now_add=True)


class DislikeCount(models.Model):  # 用于记录不喜欢的数
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 记录点赞数
    disliked_num = models.IntegerField(default=0)


class DislikeRecord(models.Model):  # 用于记录不喜欢的详细情况，比如谁在上面时间对什么标记不喜欢
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 点赞的详情
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disliked_time = models.DateTimeField(auto_now_add=True)
