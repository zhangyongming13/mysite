"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog.views import Blog_list
from .views import home

urlpatterns = [
    path('', home, name='home'),  # 根目录，把之前的博客列表换成这个
    path('admin/', admin.site.urls),
    # 结合Django根目录的urls文件，整个访问网址是
    #  http://192.168.1.247:8000/blog/1
    path('blog/', include('blog.urls')),  # 将App内创建的urls利用include进行引入
]
