from django.contrib.contenttypes.models import ContentType
from .models import LikeCount, LikeRecord, DislikeCount, DislikeRecord
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist


def SuccessResponse(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, '用户未登录')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_object = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, '对象不存在')

    is_like = request.GET.get('is_like')

    if DislikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
        return ErrorResponse(405, '你已标记为不喜欢，请先取消不喜欢再标记为喜欢！')
    else:
        if is_like == 'true':
            # 要点赞
            like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
            if created:
                # 未点赞，进行点赞
                like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
                like_count.liked_num += 1
                like_count.save()
                like_record.save()
                return SuccessResponse(like_count.liked_num)
            else:
                # 已点赞不能重复点赞
                return ErrorResponse(402, '你已经点赞')
        else:
            # 取消点赞
            if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
                like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
                like_record.delete()  # 删除对应的点赞记录
                like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
                if not created:
                    like_count.liked_num -= 1  # 点赞数减一
                    like_count.save()
                    return SuccessResponse(like_count.liked_num)
                else:
                    return ErrorResponse(404, '数据错误')
            else:
                return ErrorResponse(403, '你没有点赞，不能取消点赞')


def dislike_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, '用户未登录')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_object = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, '对象不存在')

    is_like = request.GET.get('is_dislike')

    if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
        return ErrorResponse(405, '你已标记为喜欢，请先取消喜欢再标记为不喜欢！')
    else:
        if is_like == 'true':
            # 要点赞
            dislike_record, created = DislikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
            if created:
                # 未点赞，进行点赞
                dislike_count, created = DislikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
                dislike_count.disliked_num += 1
                dislike_count.save()
                dislike_record.save()
                return SuccessResponse(dislike_count.disliked_num)
            else:
                # 已点赞不能重复点赞
                return ErrorResponse(402, '你已经点赞')
        else:
            # 取消点赞
            if DislikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
                dislike_record = DislikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
                dislike_record.delete()  # 删除对应的点赞记录
                dislike_count, created = DislikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
                if not created:
                    dislike_count.disliked_num -= 1  # 点赞数减一
                    dislike_count.save()
                    return SuccessResponse(dislike_count.disliked_num)
                else:
                    return ErrorResponse(404, '数据错误')
            else:
                return ErrorResponse(403, '你没有点赞，不能取消点赞')
