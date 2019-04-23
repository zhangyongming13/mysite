from django.shortcuts import render, get_object_or_404


# 首页的处理函数
def home(request):
    context = {}
    return render(request, 'home.html', context)
