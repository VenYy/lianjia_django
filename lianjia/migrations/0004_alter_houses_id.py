# Generated by Django 4.2.7 on 2023-11-07 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lianjia', '0003_rename_house_id_houses_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houses',
            name='id',
            field=models.CharField(db_column='id_', max_length=255, primary_key=True, serialize=False),
        ),
    ]
