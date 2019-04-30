from django.contrib import admin
from .models import Blog, BlogType


# @admin.register(Blog)将其注册到admin中
@admin.register(Blog)
class Blog_admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_delete','get_read_num', 'blog_type', 'author',  'created_time', 'last_update_time')
    ordering = ('id',)


@admin.register(BlogType)
class Blog_Type_admin(admin.ModelAdmin):
    list_display = ('id', 'blog_type')
    ordering = ('id',)


# @admin.register(ReadNum)
# class ReadNum_admin(admin.ModelAdmin):
#     list_display = ('read_num', 'blog')
