# Generated by Django 3.2.12 on 2022-07-22 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0040_alter_table_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='count',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='distance',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='distribution',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]