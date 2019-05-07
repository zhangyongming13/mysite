from django.contrib import admin
from .models import ReadNum, ReadDetail


@admin.register(ReadNum)
class ReadNum_admin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'read_num')
    # ordering = ('id',)


@admin.register(ReadDetail)
class ReadDetail_admin(admin.ModelAdmin):
    list_display = ('id', 'date', 'content_object', 'read_num')
