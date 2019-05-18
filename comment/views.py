from django.shortcuts import render, redirect, reverse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
from django.http import JsonResponse
from django.utils import timezone


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)

    # 返回给ajax的状态数据，是否完成评论
    data = {}

    if comment_form.is_valid():
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:  # 这一条是回复
            if parent.root is None:  # 被这条回复的内容是一条评论不是一条回复
                comment.root = parent
            else:  # 被这条回复的内容是一条回复，所以这条回复的root的parent的root，以此类推，直到最后一个是评论
                comment.root = parent.root
            comment.parent = parent
            comment.reply_to = parent.user  # models设置该parent的时候，外键关联User，可以可以通过parent找到user
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''

        comment.save()

        data['pk'] = comment.pk
        # 这是一条评论的话
        if comment.root is None:
            data['root_pk'] = ''
        else:
            data['root_pk'] = comment.root.pk
        # 构建返回给前端ajax的数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = timezone.localtime(comment.comment_time).strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        # return render(request, 'login_logout_error.html', {'message': '评论成功！', 'redirect_to': referer})
    else:
        data['status'] = 'ERROR'
        # 返回具体的错误信息
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
        # return render('login_logout_error.html', request, {'message': comment_form.errors, 'redirect_to': referer})
    # # 返回原来的博客页面
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    #
    # # 获取前端页面传递进来的数据
    # user = request.user
    # # 数据检查
    # if not user.is_authenticated:  # 是否真的登录了，未登录的话留下一个返回原来博客的链接
    #     return render(request, 'login_logout_error.html', {'message': '用户未登录！', 'redirect_to':referer})
    # text = request.POST.get('text', '')
    # if text.strip() == '':
    #     return render(request, 'login_logout_error.html', {'message': '提交内容为空！', 'redirect_to':referer})
    # try:
    #     object_id = int(request.POST.get('object_id', ''))
    #     # 这里传进来的时候字符串，不是博客的类
    #     content_type = request.POST.get('content_type', '')
    #
    #     # 下面是获取comment models对象中的content_object，相当于Blog.objects.get(pk=object_id)
    #     # 下面的这种写法可以让评论变得更加灵活，不单单是评论博客
    #     # 根据前端传来的blog_detail获取评论的对象content_type是Blog
    #     model_class = ContentType.objects.get(model=content_type).model_class()  # 获取所有的blog的ContentType
    #     model_object = model_class.objects.get(pk=object_id)  # 根据blog的pk确定对应的blog
    #     # 实例化一个Comment对象，数据检查通过，要完整的填好这个实例化的comment需要这些数据，具体数据可以看comment的models
    #     comment = Comment()
    #     comment.content_object = model_object
    #     comment.user = user
    #     comment.text = text
    #     comment.save()
    # except Exception as e:
    #     return render(request, 'login_logout_error.html', {'message':e, 'redirect_to':referer})
    #
    # return render(request, 'login_logout_error.html', {'message': '评论成功！', 'redirect_to':referer})
