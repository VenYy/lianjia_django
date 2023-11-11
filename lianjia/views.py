import json
import random

from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lianjia.models import Houses, City
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from lianjia.pagination import Pagination


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
    houses = Houses.objects.all()
    all_count = houses.count()
    # 如果想修改request.POST或request.GET的数据，应该先复制一份原始数据再进行修改，而不是直接修改原始数据。
    # 这是因为一旦直接修改了原始数据，那么后续的代码可能无法正确地处理这个请求。
    query_params = request.GET.copy()
    # 将其设置为可变
    query_params._mutable = True

    pager = Pagination(
        # 默认是每页显示30条数据, 最多显示11个页码
        current_page=request.GET.get('page'),
        all_count=all_count,
        base_url=request.path_info,
        query_params=query_params,
    )
    data_list = houses[pager.start:pager.end]
    return render(
        request,
        'house_list.html',
        {
            'pager': pager,
            "data_list": data_list
        }
    )
