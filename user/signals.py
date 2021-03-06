from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from notifications.signals import notify
from django.shortcuts import reverse


# 注册的时候，发送通知到刚注册的账号
@receiver(post_save, sender=User)
def send_user_save_notifications(sender, instance, **kwargs):
    # 确保是创建
    if kwargs['created']:
        verb = '注册成功！点击查看你的用户信息！'
        url = reverse('user_info')
        notify.send(instance, recipient=instance, verb=verb, action_object=instance, url=url)
