from .models import Profile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# 下面的操作相当于重写一次admin界面里面的用户，这样就可以显示我们自定义的nickname
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'nickname', 'email', 'is_staff', 'is_active', 'is_superuser')

    def nickname(self, obj):
        return obj.profile.nickname
    # 使得上面list里面的nickname显示为昵称
    nickname.short_description = '昵称'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class Profileadmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')
