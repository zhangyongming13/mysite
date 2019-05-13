from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, login, logout, register

urlpatterns = [
    path('', home, name='home'),  # 根目录，把之前的博客列表换成这个
    path('admin/', admin.site.urls),
    # 结合Django根目录的urls文件，整个访问网址是
    #  http://192.168.1.247:8000/blog/1
    path('blog/', include('blog.urls')),  # 将App内创建的urls利用include进行引入
    path('ckeditor', include('ckeditor_uploader.urls')),  # # 上传图片的url
    path('comment/', include('comment.urls')),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
