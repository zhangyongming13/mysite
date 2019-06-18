from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from notifications.signals import notify
from django.utils.html import strip_tags
import re
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import threading


# 设置一个信号接收器，接收到comemnt实例保存的信号，进行的发送站内通知的操作
# instanca相当于具体那一条评论保存了
@receiver(post_save, sender=Comment)
def send_notifications(sender, instance, **kwargs):
    # 发送站内通知
    if instance.reply_to is None:  # 这是一条评论
        # 这里comment.content_object对应的是这个评论对应的博客，然后通过动态绑定很方便的获取到作者的名称
        recipient = instance.content_object.get_user()
        if instance.content_type.model == 'blog':
            # 使用格式化函数
            verb = '{0} 评论了你的博客《{1}》'.format(
                instance.user.get_nickname_or_username(), instance.content_object.title)
        else:
            raise Exception('Unknow comment object type!')
    else:  # 这是一条回复
        recipient = instance.reply_to
        verb = '{0} 回复了你 {1}'.format(
            instance.user.get_nickname_or_username(), strip_tags(instance.parent.text))

    # url指的是这个instance对应评论或者回复（一种特殊一点的评论）对应的页面
    # #content_ + str(instance.pk)方便用户转到页面之后定位到被回复或者评论的位置
    url = instance.content_object.get_url() + '#content_' + str(instance.pk)
    # 发送通知，action_object记录这个通知是由上面触发的
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)


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


# 接收到评论成功的消息，发送邮件
@receiver(post_save, sender=Comment)
def send_email(sender, instance, **kwargs):
    # 评论完成，发送邮件通知
    if instance.parent is None:
        subject = '有人评论你的博客！'
        email = instance.content_object.get_email()
    else:
        subject = '有人回复你的评论'
        email = instance.reply_to.email

    if email != '':
        # 判断用户输入的邮箱格式是否正确
        if re.match(r'^[a-zA-Z0-9_](\w)*(_)*@[a-zA-Z0-9_]+\.[a-zA-Z]+$', email):
            # 邮件发送的内容式html模板加上参数，和之前网页是一样的
            context = {}
            # 获取comment里面的text
            context['comment_text'] = instance.text
            context['url'] = instance.content_object.get_url()
            text = render_to_string("comment/send_email.html", context)
            # 创建线程
            send_mail = SendEmail(subject, text, email)
            # 开始线程
            send_mail.start()
