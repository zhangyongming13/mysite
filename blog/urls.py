from django.urls import path
from . import views  # 引入相应的视图文件

urlpatterns = [
    path('', views.Blog_list, name='blog_list'),
    # '<int:blog_pk>'表示从网址中接收的数据
    # 结合Django根目录的urls文件，整个访问网址是
    # http://192.168.1.247:8000/blog/1
    path('<int:blog_pk>', views.Blog_detail, name='blog_detail'),
    path('blog_with_type/<int:blog_type_pk>', views.Blog_with_type, name='blog_with_type'),
    path('blog_with_date/<int:year>/<int:month>', views.blog_with_date, name='blog_with_date'),
    path('create_editor_blog/<int:blog_pk>', views.create_editor_blog, name='create_editor_blog'),
    path('delete_blog/<int:blog_pk>', views.delete_blog, name='delete_blog'),
    path('check_title_exists', views.check_title_exists, name='check_title_exists'),
    path('check_login_status', views.check_login_status, name='check_login_status'),
    path('user_blog', views.user_blog, name='user_blog'),
]
