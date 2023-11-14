from django import template

from lianjia.models import City

register = template.Library()


@register.filter(name="deal_facility")
def deal_facility(facilities):
    """分割设施列表"""
    facility_list = facilities.split(",")
    return facility_list


@register.filter(name="trans_city")
def trans_city(city):
    """将城市名称由中文转为英文"""
    city_en = City.objects.filter(city_zh=city).values()[0].get("city_en")
    return city_en


@register.filter(name="remove_param")
def remove_param(query_params, param_name):
    """移除query_params中的指定参数"""
    new_query_params = query_params.copy()
    new_query_params.pop(param_name, None)
    return new_query_params.urlencode()


@register.filter(name="remove_city")
def remove_city(query_params):
    """移除query_params中的city和district"""
    new_query_params = query_params.copy()
    new_query_params.pop("city", None)
    new_query_params.pop("district", None)
    return new_query_params.urlencode()


@register.filter(name="update_params")
def update_params(query_params, **param_dict):
    """修改query_params中的指定参数"""
    new_query_params = query_params.copy()
    print(param_dict)
