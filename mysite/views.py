from django.shortcuts import render
from read_statistics.utils import get_seven_days_data, get_today_or_yesterday_hot_blogs, get_week_or_month_hot_blogs
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from blog.views import get_common_blog_data
from django.db.models import Q


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


def search_blog(request):
    # 前端提交的方法是GET，所以使用get的形式获取前端传进来的数据
    search_word = request.GET.get('search-word', '').strip()

    # 实现多个关键字的搜索，比如两个子空格隔开 django python
    if search_word != '':
        condition = None
        # 进行分词操作
        i = 1
        search_words = ''
        for word in search_word.split(' '):
            # 组合前端显示属于什么关键字的合集
            if i > 1:
                search_words = search_words + '或' + word
            else:
                search_words = search_words + word
            i += 1
            # 利用Q关键字保存条件
            if condition is None:
                # title__icontains表示博客标题里面含有word的
                condition = Q(title__icontains=word)
            else:
                condition = condition | Q(title__icontains=word)
        # 这里的condition为(OR: ('title_icontains', '444'), ('title_icontains', '大'))
        # 相当于多个条件，中间使用的式or
        search_blogs = Blog.objects.filter(condition)
    else:
        search_blogs = []

    # 利用前面blog_list进行搜索结果的显示
    context = get_common_blog_data(request, search_blogs)
    context['search_word'] = search_words
    # context['search_blog'] = search_blogs
    return render(request, 'search_result.html', context)
