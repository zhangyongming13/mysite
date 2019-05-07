from django.shortcuts import render
from read_statistics.utils import get_seven_days_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog


# 首页的处理函数
def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, day = get_seven_days_data(blog_content_type)
    context['read_nums'] = read_nums
    context['day'] = day
    return render(request, 'home.html', context)
