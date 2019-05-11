from django import forms
from django.contrib import auth


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
