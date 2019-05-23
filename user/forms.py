from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    # 对应登录HTML里面的两个input标签
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    # widget设置form之后生成的类型
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    # 在form表单中进行数据的判断
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        # 判断为空
        if user is None:
            raise forms.ValidationError('用户名或者密码错误！')
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data


class RegForm(forms.Form):
    # 注册需要用到的信息
    username = forms.CharField(label='用户名', max_length=30, min_length=4, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码', max_length=30, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='确认密码', max_length=30, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再一次输入密码'}))

    # 单独进行每一项数据的验证
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在！')
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise  forms.ValidationError('邮箱已注册！')
        else:
            return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次密码不一致')
        else:
            return password_again


class ChangeNickname(forms.Form):
    nickname_new = forms.CharField(label='新的昵称', max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入新的昵称'}))

    # 接收view实例化ChangeNickname()时候传递进来的user参数，用来判断用户是否登录
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNickname, self).__init__(*args, **kwargs)

    # 判断用户是否登录
    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录！')
        return self.cleaned_data

    def clean_nickname_new(self):
        zhang = self.cleaned_data.get('nickname_new', '')
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('昵称不能为空！')
        # try:
        #     zhang = Profile.objects.get(nickname=nickname_new)
        #     raise forms.ValidationError('昵称已被占用！')
        # except Exception as e:
        #     pass
        if Profile.objects.filter(nickname=zhang).exists():
            raise forms.ValidationError('昵称已被占用！')
        return nickname_new
