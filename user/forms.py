from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    # 对应登录HTML里面的两个input标签
    username_or_email = forms.CharField(label='用户名或邮箱', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名或邮箱'}))
    # widget设置form之后生成的类型
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    # 在form表单中进行数据的判断
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        # 尝试用用户名进行登录
        user = auth.authenticate(username=username_or_email, password=password)
        # 判断为空
        if user is None:
            # 尝试使用邮箱进行登录
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                else:
                    raise forms.ValidationError('用户名或者邮箱或者密码错误！')
            else:
                raise forms.ValidationError('用户名或者邮箱或者密码错误！')
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data


class RegForm(forms.Form):
    # 注册需要用到的信息
    username = forms.CharField(
        label='用户名', max_length=30, min_length=4,widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入用户名'}
        )
    )
    nickname_new = forms.CharField(
        label='新的昵称', max_length=10,widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}
        )
    )
    password = forms.CharField(
        label='密码', max_length=30, min_length=6,widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码'}
        )
    )
    password_again = forms.CharField(
        label='确认密码', max_length=30, min_length=6, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再一次输入密码'}
        )
    )
    email = forms.EmailField(
        label='邮箱',widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}
        )
    )
    verification_code = forms.CharField(
        label="验证码", required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击发送验证码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

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

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '')
        if verification_code.strip() == '':
            raise forms.ValidationError('验证码不能为空！')

        # 判断验证码，// 获取之前创建验证码的时候通过session保存的验证码
        create_code = self.request.session.get('register_code', '')
        if create_code == '':
            raise forms.ValidationError('其他错误，请刷新页面重试！')
        if verification_code.lower() != create_code.lower():
            raise forms.ValidationError('验证码不正确！')
        return verification_code

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


class BindEmail(forms.Form):
    email = forms.EmailField(
        label="邮箱", widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'输入新的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label="验证码", required=False, widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击发送验证码'}
        )
    )

    # 接收view实例化ChangeNickname()时候传递进来的user参数，用来判断用户是否登录
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmail, self).__init__(*args, **kwargs)

    # 判断用户是否登录
    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录！')

        return self.cleaned_data

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '')
        if verification_code.strip() == '':
            raise forms.ValidationError('验证码不能为空！')

        # 判断验证码，// 获取之前创建验证码的时候通过session保存的验证码
        create_code = self.request.session.get('bind_email_code', '')
        if create_code == '':
            raise forms.ValidationError('其他错误，请刷新页面重试！')
        if verification_code.lower() != create_code.lower():
            raise forms.ValidationError('验证码不正确！')
        return verification_code

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被绑定，请换一个邮箱！')
        return email


class ChangeUserPassword(forms.Form):
    password = forms.CharField(
        label='原密码', max_length=30, min_length=6, widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'输入原密码'}
        )
    )

    password_new = forms.CharField(
        label='新密码', max_length=30, min_length=6, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '输入新密码'}
        )
    )

    password_new_again = forms.CharField(
        label='确认密码', max_length=30, min_length=6, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '再输入一次新密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangeUserPassword, self).__init__(*args, **kwargs)

    # 判断用户是否登录
    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录！')

        password = self.cleaned_data['password']
        user = auth.authenticate(username=self.request.user.username, password=password)
        if user is None:
            raise forms.ValidationError('原密码错误！')
        return self.cleaned_data

    def clean_password(self):
        password = self.cleaned_data['password'].strip()
        if password == '':
            raise forms.ValidationError('原密码不能为空！')
        return password

    # 判断两次输入的密码是否一致
    def clean_password_new_again(self):
        password = self.cleaned_data['password']
        password_new = self.cleaned_data['password_new']
        password_new_again = self.cleaned_data['password_new_again']

        if password_new == '' or password_new_again == '':
            raise forms.ValidationError('密码不能为空！')
        if password_new != password_new_again:
            raise forms.ValidationError('两次密码不一致！')

        if password == password_new_again:
            raise forms.ValidationError('新密码和原密码不能相同！')
        return password_new_again


class ForgetPassword(forms.Form):
    email = forms.EmailField(
        label="邮箱", widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '输入绑定的邮箱'}
        )
    )

    password_new = forms.CharField(
        label='新密码', max_length=30, min_length=6, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '输入新密码'}
        )
    )

    password_new_again = forms.CharField(
        label='确认密码', max_length=30, min_length=6, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '再输入一次新密码'}
        )
    )

    verification_code = forms.CharField(
        label="验证码", required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击发送验证码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgetPassword, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data['email']
        password_new_again = self.cleaned_data['password_new_again']
        # 检查该邮箱是否有对应的账号
        if User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username
            # 检查新的密码和原来的密码是否一致
            user = auth.authenticate(username=username, password=password_new_again)
            if user is None:
                return self.cleaned_data
            else:
                raise forms.ValidationError('新密码不能与原密码相同！')
        else:
            raise forms.ValidationError('该邮箱不存在对应的用户，请检查邮箱或者直接注册！')

    def clean_password_new_again(self):
        password_new = self.cleaned_data['password_new']
        password_new_again = self.cleaned_data['password_new_again']
        if password_new == '' or password_new_again == '':
            raise forms.ValidationError('新密码不能为空！')
        if password_new_again != password_new:
            raise forms.ValidationError('两次输入的密码不一致！')
        return password_new_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '')
        if verification_code.strip() == '':
            raise forms.ValidationError('验证码不能为空！')

        # 判断验证码，// 获取之前创建验证码的时候通过session保存的验证码
        create_code = self.request.session.get('forget_password_email_code', '')
        if create_code == '':
            raise forms.ValidationError('其他错误，请刷新页面重试！')
        if verification_code.lower() != create_code.lower():
            raise forms.ValidationError('验证码不正确！')
        return verification_code
