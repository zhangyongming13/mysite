from django.contrib import admin
from .models import ReadNum


@admin.register(ReadNum)
class ReadNum_admin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'read_num')
    # ordering = ('id',)
