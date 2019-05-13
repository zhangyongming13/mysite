from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget


# 创建评论表单
class CommentForm(forms.Form):

    # 使用ckeditor富文本编辑，设置文件在setting.py
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'))
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)

    # 接收view实例化CommenForm时候传递进来的user参数
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    # 对数据进行认证
    def clean(self):
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录！')
        try:
            # 确保能获取到博客的具体信息，这样才可以进行评论
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_object = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_object
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在！')

        return self.cleaned_data
