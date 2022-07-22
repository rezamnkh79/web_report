# Generated by Django 3.2.12 on 2022-07-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0028_point_info_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point_info',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='point_info',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=8, null=True),
        ),
    ]
