from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LikeRecord
from notifications.signals import notify
from django.utils.html import strip_tags


@receiver(post_save, sender=LikeRecord)
def send_like_notifications(sender, instance, **kwargs):
    # 发送站内通知
    if kwargs['created']:
        recipient = instance.content_object.get_user()
        if instance.content_type.model == 'blog':  # 这是一条评论
            verb = '{0} 点赞了你的博客《{1}》'.format(
                instance.user.get_nickname_or_username(), instance.content_object.title)
            url = instance.content_object.get_url()
        else:  # 这是一条回复
            verb = '{0} 点赞了你的回复 {1}'.format(
                instance.user.get_nickname_or_username(), strip_tags(instance.content_object.text))
            url = instance.content_object.get_url() + '#content_' + str(instance.content_object.pk)

        # 发送通知，action_object记录这个通知是由上面触发的
        notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)
