# Generated by Django 3.2.12 on 2022-07-21 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0035_alter_color_info_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color_info',
            name='color_range',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.ranges'),
        ),
    ]