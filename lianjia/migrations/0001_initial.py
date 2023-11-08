# Generated by Django 4.2.7 on 2023-11-07 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_en', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('city_zh', models.CharField(max_length=32, null=True, unique=True)),
            ],
            options={
                'db_table': 'lianjia_city',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_en', models.CharField(max_length=32)),
                ('district_zh', models.CharField(max_length=32, null=True, unique=True)),
                ('city_en', models.ForeignKey(db_column='city_en', null=True, on_delete=django.db.models.deletion.CASCADE, to='lianjia.city')),
            ],
            options={
                'db_table': 'lianjia_district',
            },
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=32)),
                ('district', models.CharField(max_length=32)),
                ('village_name', models.CharField(max_length=255)),
                ('lng', models.DecimalField(decimal_places=15, max_digits=19, null=True)),
                ('lat', models.DecimalField(decimal_places=15, max_digits=19, null=True)),
            ],
            options={
                'db_table': 'lianjia_village',
                'unique_together': {('city', 'district', 'village_name')},
            },
        ),
        migrations.CreateModel(
            name='Houses',
            fields=[
                ('house_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, null=True)),
                ('village_name', models.CharField(max_length=255, null=True)),
                ('img_src', models.CharField(max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('rent_type', models.CharField(max_length=32, null=True)),
                ('rooms', models.CharField(max_length=32, null=True)),
                ('direction', models.CharField(max_length=32, null=True)),
                ('floor_type', models.CharField(max_length=32, null=True)),
                ('floor_num', models.IntegerField(null=True)),
                ('facilities', models.CharField(max_length=255, null=True)),
                ('area', models.CharField(max_length=32, null=True)),
                ('city', models.ForeignKey(db_column='city', null=True, on_delete=django.db.models.deletion.CASCADE, to='lianjia.city', to_field='city_zh')),
                ('district', models.ForeignKey(db_column='district', null=True, on_delete=django.db.models.deletion.CASCADE, to='lianjia.district', to_field='district_zh')),
            ],
            options={
                'db_table': 'lianjia_houses',
            },
        ),
    ]
