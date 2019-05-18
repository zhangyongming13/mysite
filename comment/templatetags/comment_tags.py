from django import template
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag  # 进行注册操作，确保可以被其他的引用
def get_comment_count(blog, blog_id):
    blog_content_type = ContentType.objects.get_for_model(blog)
    comment_count = Comment.objects.filter(content_type=blog_content_type, object_id=blog_id).count()
    return comment_count
