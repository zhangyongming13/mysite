from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment


# 创建评论表单
class CommentForm(forms.Form):

    # 使用ckeditor富文本编辑，设置文件在setting.py
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'), error_messages={'required':'评论内容不能为空'})
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)

    # 创建回复的时候，被回复的评论/回复的ID值， attr表示的是生成前端页面的时候该元素的ID值，这样方便JQuery找到该元素
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_comment_id'}))

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

    # 对前端传来的reply_comment_id进行验证
    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错！')
        elif reply_comment_id == 0:  # 证明这是一条评论不是一条回复
            self.cleaned_data['parent'] = None
        elif reply_comment_id > 0:  # 证明这是一条回复，设置这条回复的parent,表面被回复的是谁
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错！')
        return reply_comment_id
