# Generated by Django 3.2.12 on 2022-09-17 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0056_auto_20220915_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='color_info',
            name='band',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='color_info',
            name='freq',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
