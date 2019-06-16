from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Comment(models.Model):
    # 和计数功能类似，所以使用ContentType确保可以对所有对象进行评论
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    # 记录这条评论是谁评论的
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    # 记录第一条评论，方便找到回复该评论的所有回复，和parent不同的是，parent只是该条回复是回复谁的
    root = models.ForeignKey('self', related_name="root_comment", null=True, on_delete=models.CASCADE)
    # 记录评论的上一级是什么，用于对评论的回复
    parent = models.ForeignKey('self', related_name="parent_comment", null=True, on_delete=models.CASCADE)
    # 记录这条评论式回复谁的，如果这是第一条评论，那么则为空
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    def get_user(self):
        return self.user

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
