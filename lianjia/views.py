import json
import random

from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lianjia.models import Houses, City
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    current_city = request.GET.get("current_city", "宁波")
    house_count = Houses.objects.filter(city__city_zh=current_city).all().count()
    city_list = [i[0] for i in City.objects.all().values_list("city_zh")]

    suggest_list = random.choices(Houses.objects.filter(city__city_zh=current_city).values(), k=5)
    context = {
        "house_count": house_count,
        "city_list": city_list,
        "current_city": current_city,
        "suggest_list": suggest_list
    }
    return render(request, "index.html", context)


@csrf_exempt
def search_result(request):
    if request.method == "POST":
        keyword = request.POST.get("search-input")
        data = Houses.objects.filter(
            Q(city__city_zh__contains=keyword) |
            Q(district__district_zh__contains=keyword) |
            Q(village_name__contains=keyword) |
            Q(rooms__contains=keyword)
        ).values()
        return JsonResponse({"status": 1, "data": list(data)[:8]})
    else:
        return JsonResponse({"status": 0, "error": "请求方式错误"})


# 房源列表
def house_list(request):
    houses = Houses.objects.all().values()
    paginator = Paginator(houses, 30)  # 实例化一个分页对象, 每页显示30个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        # page_obj: 分页后的对象列表，在模板中使用for循环遍历即可；
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # 如果页码超出范围，显示最后一页
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页
    context = {
        "page_obj": page_obj,
        "is_paginated": is_paginated
    }
    return render(request, "house_list.html", context)
