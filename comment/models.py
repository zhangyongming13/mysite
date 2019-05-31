import threading
import re
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


# 多线程发送邮箱验证码
class SendEmail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False,):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(  # 发送邮件
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            self.fail_silently,
            # 使用html模板
            html_message=self.text
        )


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

    def send_email(self):
        if self.parent is None:
            subject = '有人评论你的博客！'
            email = self.content_object.get_email()
        else:
            subject = '有人回复你的评论'
            email = self.reply_to.email

        if email != '':
            # 判断用户输入的邮箱格式是否正确
            if re.match(r'^[a-zA-Z0-9_](\w)*(_)*@[a-zA-Z0-9_]+\.[a-zA-Z]+$', email):
                # 邮件发送的内容式html模板加上参数，和之前网页是一样的
                context = {}
                # 获取comment里面的text
                context['comment_text'] = self.text
                context['url'] = self.content_object.get_url()
                text = render_to_string("comment/send_email.html", context)
                # 创建线程
                send_mail = SendEmail(subject, text, email)
                # 开始线程
                send_mail.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
