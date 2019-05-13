from django.shortcuts import render, redirect, reverse
from read_statistics.utils import get_seven_days_data, get_today_or_yesterday_hot_blogs, get_week_or_month_hot_blogs
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import LoginForm, RegForm


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
    # 因为在其他页面点击登录之后是get这个login页面，但是login页面提交数据的时候也是访问
    # 该页面所以，这里要根据是POST或者GET来来编写不同的方法
    # POST方法，提交数据
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        # 提交的数据没有问题，进行登录操作
        if login_form.is_valid():
            # user已经在form表单中进行进行验证，直接登录
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            # 根据进入login前的页面（也就是博客的具体页面）传入的链接，登录成功之后就返回博客
            # return redirect(request.GET.get('from', reverse('home')))
            original_url = request.GET.get('from', reverse('home'))
            return render(request, 'login_logout_error.html', {'message':'登录成功！', 'redirect_to':original_url})
    else:
        # get方法利用form表单生成对应input用于用户输入login_form
        # 实例化一个LoginForm类
        login_form = LoginForm()
    # 除非是登录成功，不然都会回到login页面，如果是在POST中，这个login_form就会携带有错误信息
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)

    # 获取到request请求头里面原本的网址信息，这样登录之后就跳回原来未登录前的页面
    referer = request.META.get('HTTP_REFERER', 'home')
    return  render(request, 'login_logout_error.html', {'message': '注销成功！', 'redirect_to':referer})


# 注册的处理方法
def register(request):
    # 和login方法类似，也需要判断式POST还是GET，POST进行账号注册，GET实例化
    # form并传递给前端页面
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']

            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()

            # 注册之后进行登录操作
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            # 传递注册之前页面的链接信息，注册通过之后可以返回相关的页面
            original_url = request.GET.get('from', reverse('home'))
            return render(request, 'login_logout_error.html', {'message': '注册成功！', 'redirect_to': original_url})
    else:
        # 实例化RegForm，传递给模板页面进行模板页面产生以及承载数据
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
