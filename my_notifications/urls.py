from django.urls import path
from . import views  # 引入相应的视图文件

urlpatterns = [
    path('', views.my_notifications, name='my_notifications'),
    path('<int:notification_pk>', views.my_notifications_middle, name='my_notifications_middle'),
    path('delete_my_read_notifications', views.delete_my_read_notifications, name='delete_my_read_notifications'),
]
