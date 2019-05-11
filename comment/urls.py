from django.urls import path
from . import views  # 引入相应的视图文件

urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment'),
]