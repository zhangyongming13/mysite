from django.shortcuts import render, get_object_or_404, reverse, redirect
from notifications.models import Notification


def my_notifications(request):
    context = {}
    return render(request, 'my_notifications/my_notifications.html', context)


# 点击消息之后，将消息unread状态修改为False
def my_notifications_middle(request, notification_pk):
    notification = get_object_or_404(Notification, pk=notification_pk)
    notification.unread = False
    notification.save()
    # 跳转到消息对应的页面中
    return redirect(notification.data['url'])


# 删除所有已读消息
def delete_my_read_notifications(request):
    # 获取用户所有已读的消息
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))
