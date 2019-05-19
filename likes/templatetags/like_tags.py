from django import template
from ..models import LikeCount, LikeRecord, DisikeRecord, DislikeCount
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag()
def get_like_num(blog):  # 返回点赞的数量
    blog_content_type = ContentType.objects.get_for_model(blog)
    like_count, created = LikeCount.objects.get_or_create(content_type=blog_content_type, object_id=blog.pk)
    return like_count.liked_num


@register.simple_tag()  # 返回点赞的情况
def get_like_status(obj, user):
    obj_content_type = ContentType.objects.get_for_model(obj)
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=obj_content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''


@register.simple_tag()
def get_dislike_num(blog):  # 返回点赞的数量
    blog_content_type = ContentType.objects.get_for_model(blog)
    dislike_count, created = DislikeCount.objects.get_or_create(content_type=blog_content_type, object_id=blog.pk)
    return dislike_count.disliked_num


@register.simple_tag()  # 返回点赞的情况
def get_dislike_status(obj, user):
    obj_content_type = ContentType.objects.get_for_model(obj)
    if not user.is_authenticated:
        return ''
    if DisikeRecord.objects.filter(content_type=obj_content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''


@register.simple_tag()
def get_content_type(obj):  # 返回对象contenttype的具体名字比如'blog'， 'comment'
    obj_content_type = ContentType.objects.get_for_model(obj).model
    return obj_content_type
