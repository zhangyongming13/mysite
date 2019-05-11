from django.shortcuts import render, redirect
from read_statistics.utils import get_seven_days_data, get_today_or_yesterday_hot_blogs, get_week_or_month_hot_blogs
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from django.contrib import auth


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


def login(request):
    referer = request.META.get('HTTP_REFERER', 'home')
    # 获取前端post进来的数据，获取不到设置为空
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    # 判断用户名和密码是否正确，使用django自带的用户系统以及认证
    user = auth.authenticate(request, username=username, password=password)

    # 获取到request请求头里面原本的网址信息，这样登录之后就跳回原来未登录前的页面
    referer = request.META.get('HTTP_REFERER', 'home')
    if user is not None:
        auth.login(request, user)
        return render(request, 'login_logout_error.html', {'message': '登录成功！', 'redirect_to':referer})  # 登录成功，跳转到首页
    else:
        return render(request, 'login_logout_error.html', {'message': '用户名或密码不正确！', 'redirect_to':referer})


def logout(request):
    auth.logout(request)

    # 获取到request请求头里面原本的网址信息，这样登录之后就跳回原来未登录前的页面
    referer = request.META.get('HTTP_REFERER', 'home')
    return  render(request, 'login_logout_error.html', {'message': '注销成功！', 'redirect_to':referer})
