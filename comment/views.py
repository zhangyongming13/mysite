from django.shortcuts import render, redirect, reverse
from .models import Comment
from django.contrib.contenttypes.models import ContentType


def update_comment(request):
    # 返回原来的博客页面
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    # 获取前端页面传递进来的数据
    user = request.user
    # 数据检查
    if not user.is_authenticated:  # 是否真的登录了，未登录的话留下一个返回原来博客的链接
        return render(request, 'login_logout_error.html', {'message': '用户未登录！', 'redirect_to':referer})
    text = request.POST.get('text', '')
    if text.strip() == '':
        return render(request, 'login_logout_error.html', {'message': '提交内容为空！', 'redirect_to':referer})
    try:
        object_id = int(request.POST.get('object_id', ''))
        # 这里传进来的时候字符串，不是博客的类
        content_type = request.POST.get('content_type', '')

        # 下面是获取comment models对象中的content_object，相当于Blog.objects.get(pk=object_id)
        # 下面的这种写法可以让评论变得更加灵活，不单单是评论博客
        # 根据前端传来的blog_detail获取评论的对象content_type是Blog
        model_class = ContentType.objects.get(model=content_type).model_class()  # 获取所有的blog的ContentType
        model_object = model_class.objects.get(pk=object_id)  # 根据blog的pk确定对应的blog
        # 实例化一个Comment对象，数据检查通过，要完整的填好这个实例化的comment需要这些数据，具体数据可以看comment的models
        comment = Comment()
        comment.content_object = model_object
        comment.user = user
        comment.text = text
        comment.save()
    except Exception as e:
        return render(request, 'login_logout_error.html', {'message':e, 'redirect_to':referer})

    return render(request, 'login_logout_error.html', {'message': '评论成功！', 'redirect_to':referer})
