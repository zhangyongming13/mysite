from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
# Create your views here.


def Blog_list(request):
    context = {}
    # 使用过滤器过滤掉标记为删除的博客，传入的是一个可迭代的对象
    context['blogs'] = Blog.objects.filter(is_delete=False)
    # 引用templates文件中的模板，content为传进模板的数据，腰围dict类型
    return render(request, "blog_list.html", context)


def Blog_detail(request, blog_pk):
    context = {}
    context['blog_detail'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog_detail.html', context)


def Blog_with_type(request, blog_type_pk):
    context ={}
    # 根据传入的blog_type_pk获取对应的BlogType类型
    blog_type_name = get_object_or_404(BlogType, pk=blog_type_pk)
    # 根据BlogType类型获得相应类型的文章
    context['blogs'] = Blog.objects.filter(blog_type=blog_type_name)
    context['blogs_type'] = blog_type_name
    context['blog_type_pk'] = blog_type_pk
    # 调用模板文件
    return render(request, 'blog_with_type.html', context)
