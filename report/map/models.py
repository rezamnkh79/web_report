
from operator import truediv
from statistics import mode
from django.db import models
from pkg_resources import require


class Poit_Info(models.Model):
    Time = models.CharField(max_length=300)
    latitude = models.DecimalField(
       max_digits=8, decimal_places=6
    )
    longitude = models.DecimalField(
       max_digits=8, decimal_places=6
    )
    Accuracy = models.IntegerField()
    Code = models.IntegerField()
    Power = models.IntegerField()
    
class Color(models.Model):
   max = models.IntegerField()
   min = models.IntegerField()
   tech = models.CharField(max_length=50,blank=True,null=True)
   color = models.CharField(max_length=200)

# class Color_Info(models.Model):
#    # paraeter = models.CharField(max_length=100)
#    color = models.CharField(max_length=100)
#    name = models.CharField(max_length=100)
#    count =models.IntegerField()
#    # color_range =  models.OneToOneField("Color",on_delete=models.CASCADE)
#    distance = models.IntegerField()
#    distribution = models.DecimalField(
#        max_digits=8, decimal_places=2,blank=True,null=True
#     )

# class Point(models.Model):
#     location = models.ListCharField(base_field=models.CharField())
class Color_param(models.Model):
      paraeter = models.CharField(max_length=100,blank=True,null=True)
      name = models.CharField(max_length=100)
      count =models.IntegerField()
      color_range =  models.OneToOneField("Color",on_delete=models.CASCADE)
      distance = models.IntegerField()
      distribution = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
