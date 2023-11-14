import json
import random

from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lianjia.models import Houses, City, District
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
def search_suggest(request):
    """首页搜索建议"""
    if request.method == "POST":
        keyword = request.POST.get("search-input")
        data = Houses.objects.filter(
            # Q对象用于创建复杂的查询条件, 可以在查询中进行逻辑判断(AND &、OR |、NOT ~)
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
    search_input = request.GET.get("param")
    city = request.GET.get("city", "")
    district = request.GET.get("district", "")
    rent_type = request.GET.get("rent_type", "")

    # 如果想修改request.POST或request.GET的数据，应该先复制一份原始数据再进行修改，而不是直接修改原始数据。
    # 这是因为一旦直接修改了原始数据，那么后续的代码可能无法正确地处理这个请求。
    query_params = request.GET.copy()
    # 将其设置为可变
    query_params._mutable = True

    # print(query_params)             # <QueryDict: {'city': ['嘉兴']}>
    # print(query_params["city"])     # 嘉兴

    # 城市列表
    city_list = list(City.objects.all().values_list("city_zh", flat=True))

    # 当前城市所对应的下级区县
    try:
        sub_districts = list(District.objects.filter(city_en=City.objects.get(city_zh=city).city_en) \
                             .values_list("district_zh", flat=True))
    except:
        sub_districts = []

    # houses = Houses.objects.all()
    query = Houses.objects

    # 输入框搜索
    if search_input:
        search_input = search_input.replace(" ", "")
        query = query.filter(
            Q(city__city_zh__contains=search_input) |
            Q(district__district_zh__contains=search_input) |
            Q(village_name__contains=search_input) |
            Q(rooms__contains=search_input)
        )

    # 按城市名称筛选
    if city:
        query = query.filter(city__city_zh=city)

    # 按区县名称筛选
    if district:
        query = query.filter(district__district_zh=district)

    # 按出租类型筛选
    if rent_type:
        query = query.filter(rent_type=rent_type)

    houses = query.all()

    all_count = houses.count()

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
            "data_list": data_list,
            "city_list": city_list,
            "sub_districts": sub_districts,
            "current_city": city,
            "district": district,
            "rent_type": rent_type,
            "query_params": query_params
        }
    )

# @csrf_exempt
# def search_result(request):
#     """房源列表页搜索结果"""
#     if request.method == "POST":
#         keyword = request.POST.get("search_input")
#         data = Houses.objects.filter(
#             Q(city__district__district_zh__contains=keyword) |
#             Q(city__city_zh__contains=keyword) |
#             Q(village_name__contains=keyword)
#         ).values()
#         return JsonResponse({"status": 1, "data": list(data)})
