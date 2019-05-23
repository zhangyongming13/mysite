from django import template
from ..models import Profile


register = template.Library()


@register.simple_tag()
def get_nickname(user):  # 返回昵称
    try:
        profile = Profile.objects.get(user=user)
        return profile.nickname
    except Exception as e:
        return ''
