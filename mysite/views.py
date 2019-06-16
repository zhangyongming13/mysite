from django.shortcuts import render
from read_statistics.utils import get_seven_days_data, get_today_or_yesterday_hot_blogs, get_week_or_month_hot_blogs
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache


# 首页的处理函数
def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, day = get_seven_days_data(blog_content_type)

    # 查看缓存中有没有相应的数据
    today_hot_blogs = cache.get('today_hot_blogs')
    if today_hot_blogs is None:
        # 获如果缓存式空的话，则调用对应方法取对应日期的访问数据
        today_hot_blogs = get_today_or_yesterday_hot_blogs(blog_content_type, 'today')
        print('计算')
        cache.set('today_hot_blogs', today_hot_blogs, 60)
    else:
        print('使用缓存')

    yesterday_hot_blogs = cache.get('yesterday_hot_blogs')
    if yesterday_hot_blogs is None:
        # 获取对应日期的访问数据的方法的调用
        yesterday_hot_blogs = get_today_or_yesterday_hot_blogs(blog_content_type, 'yesterday')
        print('计算')
        cache.set('yesterday_hot_blogs', yesterday_hot_blogs, 60)
    else:
        print('使用缓存')

    week_hot_blogs = cache.get('week_hot_blogs')
    if week_hot_blogs is None:
        # 获取对应日期的访问数据的方法的调用
        week_hot_blogs = get_week_or_month_hot_blogs('week')
        print('计算')
        cache.set('week_hot_blogs', week_hot_blogs, 60)
    else:
        print('使用缓存')

    month_hot_blogs = cache.get('month_hot_blogs')
    if month_hot_blogs is None:
        # 获取对应日期的访问数据的方法的调用
        month_hot_blogs = get_week_or_month_hot_blogs('month')
        print('计算')
        cache.set('month_hot_blogs', month_hot_blogs, 60)
    else:
        print('使用缓存')
    # yesterday_hot_blogs = get_today_or_yesterday_hot_blogs(blog_content_type, 'yesterday')
    # week_hot_blogs = week_hot_blogs('week')
    # month_hot_blogs = get_week_or_month_hot_blogs('month')
    context['read_nums'] = read_nums
    context['day'] = day
    context['today_hot_blogs'] = today_hot_blogs
    context['yesterday_hot_blogs'] = yesterday_hot_blogs
    context['week_hot_blogs'] = week_hot_blogs
    context['month_hot_blogs'] = month_hot_blogs
    return render(request, 'home.html', context)


def my_notifications(request):
    context = {}
    return render(request, 'my_notifications.html', context)
