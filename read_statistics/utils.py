from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum


# 当被调用的时候，说明该博文被阅读了一次，所以要进行阅读数加1的操作
def read_statistics_add_times(request, blog, blog_pk):
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        ct = ContentType.objects.get_for_model(blog)
        if ReadNum.objects.filter(content_type=ct, object_id=blog_pk).count():
            readnum = ReadNum.objects.get(content_type=ct, object_id=blog_pk)
        else:
            readnum = ReadNum(content_type=ct, object_id=blog_pk)
        readnum.read_num += 1
        readnum.save()
