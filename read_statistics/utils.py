import datetime, pytz
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from read_statistics.models import ReadNum, ReadDetail
from django.db.models import Sum
from blog.models import Blog


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
        now = timezone.now()
        # 切换本地的时区
        today = timezone.localtime(now).date()
        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=blog_pk, date=today)
        readdetail.read_num += 1
        readdetail.save()


# 返回最近七天每一天的访问数
def get_seven_days_data(content_type):
    now = timezone.now()
    # 切换本地的时区
    today = timezone.localtime(now).date()
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


# 获取今天或者昨天访问数据的方法
def get_today_or_yesterday_hot_blogs(content_type, day_flag):
    now = timezone.now()
    # 切换本地的时区
    today = timezone.localtime(now).date()
    if day_flag == 'yesterday':
        today = today - datetime.timedelta(days=1)
    # 利用ContentType的反向api功能访问统计数据
    # values表示Blog需要传递出去的值
    # annotate表示对数据进行聚合
    today_hot_blogs = Blog.objects.filter(read_details__date=today) \
                                  .values('id', 'title') \
                                  .annotate(read_num_sum=Sum('read_details__read_num')) \
                                  .order_by('-read_num_sum')[:4]
    # today_hot_blogs = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')[:4]
    return today_hot_blogs


# 获取七日或者30天内访问数据的方法
def get_week_or_month_hot_blogs(flag):
    now = timezone.now()
    # 切换本地的时区
    today = timezone.localtime(now).date()
    if flag == 'week':
        date = today - datetime.timedelta(days=7)
    elif flag == 'month':
        date = today - datetime.timedelta(days=30)
    blogs = Blog.objects.filter(read_details__date__lte=today, read_details__date__gt=date) \
                        .values('id', 'title') \
                        .annotate(read_num_sum=Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')[:4]
    return blogs
