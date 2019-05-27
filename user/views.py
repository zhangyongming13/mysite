from django.shortcuts import render, reverse
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import LoginForm, RegForm, ChangeNickname, BindEmail, ChangeUserPassword
from django.http import JsonResponse
from .models import Profile
from django.core.mail import send_mail
import re
import string
import random
import time


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    # 提交的数据没有问题，进行登录操作
    if login_form.is_valid():
        # user已经在form表单中进行进行验证，直接登录
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


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
            if re.match(r'.*/user/register/.*', original_url):
                return render(request, 'user/login_logout_error.html',
                              {'message': '登录成功！', 'message1': '首页...', 'redirect_to': '/'})
            return render(request, 'user/login_logout_error.html', {'message':'登录成功！', 'message1':'原来的页面...', 'redirect_to':original_url})
    else:
        # get方法利用form表单生成对应input用于用户输入login_form
        # 实例化一个LoginForm类
        login_form = LoginForm()
    # 除非是登录成功，不然都会回到login页面，如果是在POST中，这个login_form就会携带有错误信息
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


def logout(request):
    auth.logout(request)

    # 获取到request请求头里面原本的网址信息，这样登录之后就跳回原来未登录前的页面
    referer = request.META.get('HTTP_REFERER', 'home')
    # zhang = re.split(r'/', referer)'user_info'
    if re.match(r'.*user_info.*', referer):
        return render(request, 'user/login_logout_error.html', {'message':'注销成功！返回首页', 'message1':'首页...', 'redirect_to':'/'})
    return  render(request, 'user/login_logout_error.html', {'message': '注销成功！', 'message1':'原来的页面...', 'redirect_to':referer})


# 注册的处理方法
def register(request):
    original_url = request.GET.get('from', reverse('home'))
    # 和login方法类似，也需要判断式POST还是GET，POST进行账号注册，GET实例化
    # form并传递给前端页面
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            nickname = reg_form.cleaned_data['nickname_new']

            # 创建用户
            user = User.objects.create_user(username, email, password)

            # 昵称的保存方法，先创建自定义模型里面包含昵称的类
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = nickname

            user.save()
            profile.save()

            # 注册之后进行登录操作
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            # 传递注册之前页面的链接信息，注册通过之后可以返回相关的页面
            original_url = request.GET.get('from', reverse('home'))
            if re.match(r'.*/user/login/.*', original_url):
                return render(request, 'user/login_logout_error.html',
                              {'message': '注册成功！', 'message1': '首页...', 'redirect_to': '/'})
            return render(request, 'user/login_logout_error.html', {'message': '注册成功！','message1':'原来的页面', 'redirect_to': original_url})
    else:
        # 实例化RegForm，传递给模板页面进行模板页面产生以及承载数据
        reg_form = RegForm()
    context = {}
    context['return_back'] = original_url
    context['page_title'] = '绑定邮箱'
    context['forms_title'] = '输入邮箱'
    context['submit_text'] = '绑定'
    context['forms'] = reg_form
    return render(request, 'user/register.html', context)


def user_info(request):  # user的信息都可以在前端页面获取，这里不用返回数据
    context = {}
    return render(request, 'user/user_info.html', context)


def change_nickname(request):
    original_url = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        forms = ChangeNickname(request.POST, user=request.user)
        if forms.is_valid():
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = forms.cleaned_data['nickname_new']
            profile.save()
            return render(request, 'user/login_logout_error.html', {'message':'昵称修改成功','message1':'原来的页面', 'redirect_to':original_url})
    else:
        forms = ChangeNickname()
    context = {}
    context['return_back'] = original_url
    context['page_title'] = '修改昵称'
    context['forms_title'] = '输入新的昵称'
    context['submit_text'] = '修改'
    context['forms'] = forms
    return render(request, 'user/forms.html', context)


def bind_email(request):
    original_url = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        forms = BindEmail(request.POST, request=request)
        if forms.is_valid():
            email = forms.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return render(request, 'user/login_logout_error.html',
                          {'message': '邮箱绑定成功', 'message1': '原来的页面', 'redirect_to': original_url})
    else:
        # 方法为GET。这创建BindEmail表单传给前段模板
        forms = BindEmail()
    context = {}
    context['return_back'] = original_url
    context['page_title'] = '绑定邮箱'
    context['forms_title'] = '输入邮箱'
    context['submit_text'] = '绑定'
    context['forms'] = forms
    return render(request, 'user/email.html', context)


def send_verification_code(request):
    data = {}
    email = request.GET.get('email', '')
    if User.objects.filter(email=email).exists():
        data['status'] = 'ERROR'
        data['message'] = '邮箱已被占用！'
        return JsonResponse(data)

    # 对验证码发送时间进行判断，避免验证码发送太频繁
    now = int(time.time())
    send_code_time = int(request.session.get('send_code_time', 0))
    if now - send_code_time <= 30:
        data['status'] = 'ERROR'
        data['message'] = '验证码发送太频繁！请30秒后重试。'
    else:
        request.session['send_code_time'] = now

        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['bind_email_code'] = code  # 利用session来保存这个验证码，验证需要用到
        if email != '':
            send_mail(  # 发送邮件
                '绑定邮箱',
                '验证码：%s' % code,
                '790454963@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
        else:
            data['status'] = 'ERROR'
            data['message'] = '邮箱不能为空！'
    return JsonResponse(data)


def change_user_password(request):
    # original_url = request.GET.get('from', reverse('home'))
    data = {}
    if request.method == 'POST':
        # 把前端传入的数据交给form进行数据的验证
        forms = ChangeUserPassword(request.POST, request=request)
        if forms.is_valid():
            password_new = forms.cleaned_data['password_new_again']
            try:
                user = User.objects.get(username=request.user.username)
                user.set_password(password_new)
                user.save()
                # 修改密码之后退出登录
                auth.logout(request)
                return render(request, 'user/login_logout_error.html',
                              {'message': '密码修改成功', 'message1': '登录页面', 'redirect_to': '/user/login/?from=/'})
            except Exception as e:
                data['status'] = 'ERROR'
                data['message'] = e
    else:
        forms = ChangeUserPassword()
    context = {}
    # context['return_back'] = original_url
    context['page_title'] = '修改密码'
    context['forms_title'] = '输入原密码和新密码'
    context['submit_text'] = '修改'
    context['forms'] = forms
    return render(request, 'user/change_password.html', context)
