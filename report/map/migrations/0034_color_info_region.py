# Generated by Django 3.2.12 on 2022-07-07 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0033_static_info_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='color_info',
            name='region',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
