from django.db import models


class City(models.Model):
    city_en = models.CharField(max_length=32, primary_key=True)
    city_zh = models.CharField(max_length=32, null=True, unique=True)

    class Meta:
        db_table = 'city'


class District(models.Model):
    city_en = models.ForeignKey(City, on_delete=models.CASCADE, db_column='city_en', null=True)
    district_en = models.CharField(max_length=32)
    district_zh = models.CharField(max_length=32, null=True, unique=True)

    class Meta:
        db_table = 'district'


class Houses(models.Model):
    id = models.CharField(max_length=255, primary_key=True, db_column="id_")
    title = models.CharField(max_length=255, null=True)
    village_name = models.CharField(max_length=255, null=True)
    img_src = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    rent_type = models.CharField(max_length=32, null=True)
    rooms = models.CharField(max_length=32, null=True)
    direction = models.CharField(max_length=32, null=True)
    floor_type = models.CharField(max_length=32, null=True)
    floor_num = models.IntegerField(null=True)
    facilities = models.CharField(max_length=255, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, db_column='city', to_field='city_zh', null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, db_column='district', to_field='district_zh',
                                 null=True)
    area = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = 'houses'


class Village(models.Model):
    city = models.CharField(max_length=32)
    district = models.CharField(max_length=32)
    village_name = models.CharField(max_length=255)
    lng = models.DecimalField(max_digits=19, decimal_places=15, null=True)
    lat = models.DecimalField(max_digits=19, decimal_places=15, null=True)

    class Meta:
        db_table = 'village'
        unique_together = (('city', 'district', 'village_name'),)
