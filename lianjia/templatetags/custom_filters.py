from django import template

from lianjia.models import City

register = template.Library()


# 分割设施列表
@register.filter(name="deal_facility")
def deal_facility(facilities):
    facility_list = facilities.split(",")
    return facility_list


# 将城市名称由中文转为英文
@register.filter(name="trans_city")
def trans_city(city):
    city_en = City.objects.filter(city_zh=city).values()[0].get("city_en")
    return city_en
