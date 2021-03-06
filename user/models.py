from django.db import models
from django.contrib.auth.models import User
from types import MethodType
from django.conf import settings


class Profile(models.Model):
    # 设置一对一的profile，表明一个user只能有一个别名
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, verbose_name='昵称')
    avatar = models.ImageField(upload_to=settings.AVATAR_ROOT, default=settings.AVATAR_ROOT_DEFAULT)

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)


# 进行动态绑定，让User含有get_nickname，比自定义模板标签更加简洁
def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


def has_nickname(self):
    return Profile.objects.filter(user=self).exists()


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


# 自定义模板标签，返回用户头像路径
def get_avatar_url(self):
    try:
        user_avatar = Profile.objects.get(user=self)
        return str(user_avatar.avatar)
    except:
        return settings.AVATAR_ROOT_DEFAULT


User.get_avatar_url = get_avatar_url
User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username
