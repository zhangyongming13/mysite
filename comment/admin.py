from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class Comment_admin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'user', 'comment_time', 'text')
