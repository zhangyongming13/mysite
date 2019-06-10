from django import forms
from .models import BlogType, Blog
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CreateBlogForm(forms.Form):
    title = forms.CharField(label='博客标题', max_length=30, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'size':30}))

    # 使用ModelChoiceFIeld，提供下拉菜单选项，queryset表示从数据中获取
    blog_type = forms.ModelChoiceField(label='博客类型', queryset=BlogType.objects.all())

    # form使用CKEditorUploadingWidget，确保也可以使用上传图片的功能
    text = forms.CharField(label='博客正文', widget=CKEditorUploadingWidget(config_name='create_blog'))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(CreateBlogForm, self).__init__(*args, **kwargs)

    # 判断用户是否登录
    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录！')
        return self.cleaned_data

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if title.strip() == '':
            raise forms.ValidationError('博客标题不能为空')
        if Blog.objects.filter(title=title).exists():
            raise forms.ValidationError('已存在该标题的博客，请换一个标题')
        return title

    def clean_blog_type(self):
        blog_type = self.cleaned_data.get('blog_type', '')
        if blog_type != '':
            if BlogType.objects.filter(blog_type=blog_type).exists():
                return blog_type
        return forms.ValidationError('博客类型不能为空或类型不存在！')

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if text.strip() == '':
            return forms.ValidationError('博客内容不能为空')
        return text
