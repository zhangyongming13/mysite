from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.conf import settings
# Create your views here.


def Blog_list(request):
    context = {}
    # 使用过滤器过滤掉标记为删除的博客，传入的是一个可迭代的对象
    blogs_all_list = Blog.objects.filter(is_delete=False)
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

    context['total_page'] = paginator.num_pages  # 总共有多少页
    context['page_list'] = page_list  # 页码列表
    context['page_of_blogs'] = page_of_blogs  # 博客的内容
    # 引用templates文件中的模板，content为传进模板的数据，腰围dict类型
    context['blog_type'] = BlogType.objects.all()
    context['blog_count'] = paginator.count  # 博客的总数
    return render(request, "blog/blog_list.html", context)
    # 如果把某些App的模板文件放在全局模板文件夹中的某一个文件夹，就要设置该文件夹，不然找不到模板文件


def Blog_detail(request, blog_pk):
    context = {}
    context['blog_detail'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog/blog_detail.html', context)


def Blog_with_type(request, blog_type_pk):
    context ={}
    # 根据传入的blog_type_pk获取对应的BlogType类型
    blog_type_name = get_object_or_404(BlogType, pk=blog_type_pk)
    # 根据BlogType类型获得相应类型的文章
    blog_with_type_all = Blog.objects.filter(blog_type=blog_type_name)

    # 博客分类页面也要引进分页按钮
    paginator = Paginator(blog_with_type_all, settings.EACH_PAGE_BLOG_NUMBER)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
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

    context['total_page'] = paginator.num_pages
    context['page_list'] = page_list
    context['page_of_blogs'] = page_of_blogs
    context['blogs_type'] = blog_type_name
    context['blog_type_pk'] = blog_type_pk
    context['blog_count'] = paginator.count
    context['blog_type'] = BlogType.objects.all()
    # 调用模板文件
    return render(request, 'blog/blog_with_type.html', context)
