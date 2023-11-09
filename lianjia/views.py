import json
import random

from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lianjia.models import Houses, City


# Create your views here.


def index(request):
    current_city = request.GET.get("current_city", "宁波")
    house_count = Houses.objects.filter(city__city_zh=current_city).all().count()
    city_list = [i[0] for i in City.objects.all().values_list("city_zh")]
    suggest_list = random.choices(Houses.objects.filter(city__city_zh=current_city).values(), k=5)
    return render(request, "index.html", {
        "house_count": house_count,
        "city_list": city_list,
        "current_city": current_city,
        "suggest_list": suggest_list
    })


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
    return render(request, "house_list.html")