from django import template

register = template.Library()


# 分割设施列表
@register.filter(name="deal_facility")
def deal_facility(facilities):
    facility_list = facilities.split(",")
    return facility_list
