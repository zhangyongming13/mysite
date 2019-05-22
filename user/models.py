from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # 设置一对一的profile，表明一个user只能有一个别名
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, verbose_name='昵称')

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)
