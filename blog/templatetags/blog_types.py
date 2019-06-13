from django import template
from ..models import BlogType


register = template.Library()


@register.simple_tag
def get_all_blog_type():
    blog_type = BlogType.objects.filter()
    return blog_type
