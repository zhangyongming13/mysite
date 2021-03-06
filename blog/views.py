from django.shortcuts import render, get_object_or_404, reverse, render_to_response
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.db.models import Count
from django.conf import settings
from read_statistics.utils import read_statistics_add_times
from .forms import CreateBlogForm
from django.http import JsonResponse
from user.forms import LoginForm
# from user.forms import LoginForm
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm
from django.views.decorators.csrf import csrf_exempt


def get_common_blog_data(request, blogs_all_list):
    context = {}
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOG_NUMBER)  # 进行分页
    page_num = request.GET.get('page', 1)  # 获取网页GET方法传进来的页数，默认是1
    page_of_blogs = paginator.get_page(page_num)  # 获取该页的博客
    current_page_num = page_of_blogs.number

    # 获取当前页面前后两个的页码范围
    page_list = list(range(max(current_page_num - 2, 1), min(paginator.num_pages + 1, current_page_num + 3)))

    # 添加首尾两页以及省略号
    if page_list[0] - 1 >= 2:
        page_list.insert(0, '...')
    if paginator.num_pages - page_list[-1] >= 2:
        page_list.append('...')
    if page_list[0] != 1:
        page_list.insert(0, 1)
    if page_list[-1] != paginator.num_pages:
        page_list.append(paginator.num_pages)

    # 获取博客不同类型数量
    '''BlogType.objects.annotate(blog_count=Count('blog'))表示BlogType中的类型在
    blog(BlogType和Blog有外键关联)Blog的小写的数量,先使用filter过滤已经逻辑删除的博客
    '''
    blog_type_count = BlogType.objects.filter(blog__is_delete=False).annotate(blog_count=Count('blog'))
    # blog_type = BlogType.objects.all()
    # blog_types_list = []
    # for i in blog_type:
    #     i.blog_count = Blog.objects.filter(blog_type=i).count()
    #     blog_types_list.append(i)

    # 获取时间对应的博客数量
    blog_date = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_date_dict = {}
    # i为年和月组成的日期分类
    for i in blog_date:
        blog_count = Blog.objects.filter(created_time__year=i.year, created_time__month=i.month, is_delete=False).count()
        # 利用字典保存该日期分类对应的数量，后面for循环取出的时候要添加items
        blog_date_dict[i] = blog_count

    context['total_page'] = paginator.num_pages  # 总共有多少页
    context['page_list'] = page_list  # 页码列表
    context['page_of_blogs'] = page_of_blogs  # 该页博客的内容
    context['blog_type'] = blog_type_count  # 获取所有的类型
    # context['blog_type'] = BlogType.objects.all()  # 获取所有的类型
    context['blog_count'] = paginator.count  # 博客的总数
    # 返回一个年月的日期
    context['blog_date'] = blog_date_dict
    return context


def Blog_list(request):
    # 使用过滤器过滤掉标记为删除的博客，传入的是一个可迭代的对象
    blogs_all_list = Blog.objects.filter(is_delete=False)
    context = get_common_blog_data(request, blogs_all_list)
    return render(request, "blog/blog_list.html", context)
    # 如果把某些App的模板文件放在全局模板文件夹中的某一个文件夹，就要设置该文件夹，不然找不到模板文件


def Blog_with_type(request, blog_type_pk):
    # 根据传入的blog_type_pk获取对应的BlogType类型
    blog_type_name = get_object_or_404(BlogType, pk=blog_type_pk)
    # 根据BlogType类型获得相应类型的文章
    blog_with_type_all = Blog.objects.filter(blog_type=blog_type_name, is_delete=False)
    context = get_common_blog_data(request, blog_with_type_all)
    context['blogs_type'] = blog_type_name
    context['blog_type_pk'] = blog_type_pk
    return render(request, 'blog/blog_with_type.html', context)


def blog_with_date(request, year, month):
    # 根据BlogType类型获得相应类型的文章
    blog_with_date_all = Blog.objects.filter(created_time__year=year, created_time__month=month, is_delete=False)
    context = get_common_blog_data(request, blog_with_date_all)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    context['blog_year'] = year
    context['blog_month'] = month
    return render(request, 'blog/blog_with_date.html', context)


def Blog_detail(request, blog_pk):
    context = {}
    blog_detail = get_object_or_404(Blog, pk=blog_pk)

    # 获取对应博客的评论内容
    # blog_content_type = ContentType.objects.get_for_model(blog_detail)

    # 取到评论的第一条（不包括评论下面的回复）
    # comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog_detail.pk, parent=None)
    # context['comments'] = comments.order_by('-comment_time')
    # 初始化的时候，将用于记录该评论/回复（根据reply_comment_id确定）
    # context['comment_form'] = CommentForm(
    #     initial={'content_type': blog_content_type.model, 'object_id': blog_pk, 'reply_comment_id': 0})

    # 调用计数模块里面的方法进行博客阅读数的增加
    read_statistics_add_times(request, blog_detail, blog_pk)

    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog_detail.created_time, is_delete=False).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog_detail.created_time, is_delete=False).first()
    context['blog_detail'] = blog_detail
    # context['login_form'] = LoginForm()

    # 获取评论的博客的详情，创建博客评论的时候可以一一对应
    # comment_data = {}
    # comment_data['content_type'] = blog_content_type.model
    # comment_data['object_id'] = blog_pk

    response = render(request, 'blog/blog_detail.html', context)

    # 设置发送给浏览器的cookie内容，cookie超时时间默认值，或者浏览器关闭的时候cookie才会失效
    response.set_cookie('blog_%s_readed' % blog_pk, 'true')
    return response


# 获取修改或者新增博客相同的数据
def get_common_data_crete_editor_blog(request, blog_pk):
    context ={}
    context['error'] = ''
    # 发表新博客的情况
    if blog_pk == 0:
        # 　方法为ｇｅｔ的时候就是需要新实例化有个表单，不然就是原来的
        forms = CreateBlogForm()
        context['page_title'] = '创建新的博客'
        context['forms_title'] = '创建新的博客'
        context['create_editor_flag'] = 0
    else:
        # 表示这是修改博客的情况
        try:
            blog = get_object_or_404(Blog, pk=blog_pk)
            # 初始化form表单，获取要修改blog的数据
            forms = CreateBlogForm(
                initial={'title': blog.title, 'blog_type': blog.blog_type, 'text': blog.content})
            context['page_title'] = '修改博客'
            context['forms_title'] = '修改博客'
            context['create_editor_flag'] = blog_pk

            # 修改的博客和登录的用户对不上，拒绝修改博客
            if request.user != blog.author:
                context['error'] = '您没有权限修改该博客，'
        except Exception as e:

            # 要修改的博客找不到
            forms = CreateBlogForm()
            context['error'] = '没找到要修改的博客，'
    context['create_blog_form'] = forms
    context['submit_text'] = '提交'
    return context


# 创建博客
def create_editor_blog(request, blog_pk):
    original_url = request.GET.get('from', reverse('home'))
    context = {}
    if request.method == 'POST':

        # 实例化这个表单，如果下面的验证出现问题的话，传给前端页面的这个forms就带有相关的错误信息了
        forms = CreateBlogForm(request.POST, request=request, blog_pk=blog_pk)
        if forms.is_valid():
            title = forms.cleaned_data['title']
            blog_type = forms.cleaned_data['blog_type']
            text = forms.cleaned_data['text']

            if blog_pk == 0:
                # 创建新的博客，使用create
                blog = Blog.objects.create(title=title, blog_type=blog_type, content=text, author=request.user, )
                now_blog_url = '/blog/' + str(blog.pk)  # 翻遍转到新的博客的详情页
                return render(request, 'user/login_logout_error.html',
                              {'message': '博客创建成功，', 'message1': '新增的博客详情页', 'redirect_to': now_blog_url})
            else:
                try:
                    # 根据blog_pk获取博客，然后进行修改
                    blog = get_object_or_404(Blog, pk=blog_pk)
                    now_blog_url = '/blog/' + str(blog.pk)
                    if blog.author == request.user:
                        blog.title = title
                        blog.blog_type = blog_type
                        blog.content = text
                        blog.save()
                        return render(request, 'user/login_logout_error.html',
                                    {'message': '博客修改成功，', 'message1': '修改的博客详情页', 'redirect_to': now_blog_url})
                    else:
                        return render(request, 'user/login_logout_error.html',
                                      {'message': '您没有权限修改该博客，', 'message1': '跳转到首页', 'redirect_to': '/'})
                except Exception as e:
                    return render(request, 'user/login_logout_error.html',
                                  {'message': '没找到要修改的博客，', 'message1': '跳转到首页', 'redirect_to': '/'})
        else:
            # form表单验证不通过的时候，重新渲染页面
            context = get_common_data_crete_editor_blog(request, blog_pk)
            context['create_blog_form'] = forms
    # 初始化发表或者修改页面
    else:
        context = get_common_data_crete_editor_blog(request, blog_pk)

    # 判断修改的博客是否存在，或者要修改的博客作者和登录的人是否一致
    if context['error'] != '':
        return render(request, 'user/login_logout_error.html',
                                  {'message': context['error'], 'message1': '跳转到首页', 'redirect_to': '/'})
    context['return_back'] = original_url

    # 这个表单有可能是上面is_valid不通过带有错误新的的form，也可能式新建的
    return render(request, 'blog/create_blog.html', context)


def delete_blog(request, blog_pk):
    try:
        blog = get_object_or_404(Blog, pk=blog_pk)

        # 判断被删除博客的作者和当前登录用户是否一致
        if blog.author == request.user:
            blog.is_delete = True
            blog.save()
            return render(request, 'user/login_logout_error.html',
                          {'message': '删除博客成功，', 'message1': '跳转到用户博客列表', 'redirect_to': '/blog/user_blog'})
        else:
            return render(request, 'user/login_logout_error.html',
                          {'message': '非法删除请求，', 'message1': '跳转到首页', 'redirect_to': '/'})
    except Exception as e:
        return render(request, 'user/login_logout_error.html',
                      {'message': '删除博客失败，', 'message1': '跳转到首页', 'redirect_to': '/'})


# 实时检查博客标题是否被暂用的方法
def check_title_exists(request):
    data = {}
    title = request.GET.get('title')
    if Blog.objects.filter(title=title, is_delete=False).exists():
        data['status'] = 'ERROR'
        data['message'] = '已存在该标题的博客，请换个标题！'
    else:
        data['status'] = 'SUCCESS'
    return JsonResponse(data)


# 检查用户是否登录
def check_login_status(request):
    data = {}
    # user = request.GET.get('request_user')
    if request.user.is_authenticated:
       data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


# 获取当前用户的所有博客
def user_blog(request):
    if request.user.is_authenticated:
        # 获取当前用户的所有博客
        user_blogs = Blog.objects.filter(author=request.user.pk, is_delete=False)

        # 利用所有博客获取一些公共的数据比如博客的分类，日期分类等，之所以需要这些信息
        # 是因为继承的式blog_list.html的模板，所以需要这些信息
        context = get_common_blog_data(request, user_blogs)

        username = request.user.username
        # context['page_of_blogs'] = user_blogs
        context['user_name'] = username
        return render(request, 'blog/user_blog.html', context)
