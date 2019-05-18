from django import template
from comment.models import Comment
from ..forms import CommentForm
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag  # 进行注册操作，确保可以被其他的引用
def get_comment_count(blog):  # 获取评论数
    blog_content_type = ContentType.objects.get_for_model(blog)
    comment_count = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk).count()
    return comment_count


@register.simple_tag
def get_comment_form(blog):  # 生成comment_form,用于前端页面进行渲染
    blog_content_type = ContentType.objects.get_for_model(blog)
    comment_form = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog.pk, 'reply_comment_id': 0})
    return comment_form


@register.simple_tag
def get_comment(blog):  # 获取评论不包括回复parent=None
    blog_content_type = ContentType.objects.get_for_model(blog)
    comment = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)
    result = comment.order_by('-comment_time')
    return result
