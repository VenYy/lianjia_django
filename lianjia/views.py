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
    args_city = request.GET.get("city", "")
    args_district = request.GET.get("district", "")
    args_rent_type = request.GET.get("rent_type")
    args_rooms = request.GET.get("rooms")
    args_direction = request.GET.get("direction")
    args_price = request.GET.get("price")

    # 如果想修改request.POST或request.GET的数据，应该先复制一份原始数据再进行修改，而不是直接修改原始数据。
    # 这是因为一旦直接修改了原始数据，那么后续的代码可能无法正确地处理这个请求。
    query_params = request.GET.copy()
    # 将其设置为可变
    query_params._mutable = True

    # print(query_params)             # <QueryDict: {'city': ['嘉兴']}>
    # print(query_params["city"])     # 嘉兴

    # 出租类型["整租", "合租"]
    rent_type_list = list(Houses.objects.values_list("rent_type", flat=True).distinct())
    # 城市列表
    city_list = list(City.objects.all().values_list("city_zh", flat=True))
    # 当前城市所对应的下级区县
    try:
        sub_districts = list(District.objects.filter(city_en=City.objects.get(city_zh=args_city).city_en) \
                             .values_list("district_zh", flat=True))
    except:
        sub_districts = []
    # 户型列表
    rooms_list = ["1室", "2室", "3室", "4室", "5室"]
    # 朝向列表
    direction_list = ["东", "西", "南", "北", "南/北", "其他"]
    # 价格列表
    price_list = ["0-1000元", "1000-2000元", "2000-3000元", "3000-4000元", "4000-5000元", "5000元以上"]

    # 查询对象
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
    if args_city:
        query = query.filter(city__city_zh=args_city)

    # 按区县名称筛选
    if args_district:
        query = query.filter(district__district_zh=args_district)

    # 按出租类型筛选
    if args_rent_type:
        query = query.filter(rent_type=args_rent_type)

    # 按户型筛选
    if args_rooms:
        query = query.filter(rooms__contains=args_rooms)

    # 按朝向筛选
    if args_direction:
        if args_direction == "其他":
            query = query.exclude(direction__in=direction_list)
        else:
            query = query.filter(direction=args_direction)

    # 按价格区间筛选
    if args_price:
        if args_price == "0-1000元":
            query = query.filter(price__lte=1000)
        elif args_price == "1000-2000元":
            query = query.filter(price__gte=1000, price__lte=2000)
        elif args_price == "2000-3000元":
            query = query.filter(price__gte=2000, price__lte=3000)
        elif args_price == "3000-4000元":
            query = query.filter(price__gte=3000, price__lte=4000)
        elif args_price == "4000-5000元":
            query = query.filter(price__gte=4000, price__lte=5000)
        elif args_price == "5000元以上":
            query = query.filter(price__gte=5000)

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
            "all_count": all_count,
            "args_city": args_city,
            "args_district": args_district,
            "data_list": data_list,
            "city_list": city_list,
            "sub_districts": sub_districts,
            "rent_type_list": rent_type_list,
            "rooms_list": rooms_list,
            "direction_list": direction_list,
            "price_list": price_list,
            "current_city": args_city,
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
