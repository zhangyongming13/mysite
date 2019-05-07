import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from read_statistics.models import ReadNum, ReadDetail
from django.db.models import Sum


# 当被调用的时候，说明该博文被阅读了一次，所以要进行阅读数加1的操作
def read_statistics_add_times(request, blog, blog_pk):
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        ct = ContentType.objects.get_for_model(blog)
        # if ReadNum.objects.filter(content_type=ct, object_id=blog_pk).count():
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=blog_pk)
        # else:
        #     readnum = ReadNum(content_type=ct, object_id=blog_pk)

        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=blog_pk)
        if not created:
            print('不存在，则创建！')
        readnum.read_num += 1
        readnum.save()

        # 对同一篇博客在不同的日期分别进行计数
        # if ReadDetail.objects.filter(content_type=ct, object_id=blog_pk, data=timezone.now().date()).count():
        #     readdetail = ReadDetail.objects.get(content_type=ct, object_id=blog_pk, data=timezone.now().data())
        # else:
        #     readdetail = ReadDetail(content_type=ct, object_id=blog_pk, data=timezone.now().date())

        # date()表示只需要取出对应的时间，当天的阅读数页
        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=blog_pk, date=timezone.now().date())
        readdetail.read_num += 1
        readdetail.save()


# 返回最近七天每一天的访问数
def get_seven_days_data(content_type):
    today = timezone.now().date()
    read_nums = []
    day = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        day.append(date.strftime('%m/%d'))
        rds = ReadDetail.objects.filter(content_type=content_type, date=date)
        # rds = ReadDetail.objects.all()
        result = rds.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums, day
