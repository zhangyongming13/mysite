from django.contrib import admin
from .models import LikeRecord, LikeCount


@admin.register(LikeRecord)
class LikeRecord_admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'liked_time')


@admin.register(LikeCount)
class LikeCount_admin(admin.ModelAdmin):
    list_display = ('id', 'liked_num')
