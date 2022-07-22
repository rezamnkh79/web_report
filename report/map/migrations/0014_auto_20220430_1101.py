# Generated by Django 3.2.12 on 2022-04-30 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0013_adhar_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color_param',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('count', models.IntegerField()),
                ('distance', models.IntegerField()),
                ('distribution', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('color_range', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='map.color')),
            ],
        ),
        migrations.DeleteModel(
            name='Adhar',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
