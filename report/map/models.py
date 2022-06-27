
from operator import truediv
from statistics import mode, variance
from django.db import models
from pkg_resources import require


class Point_Info(models.Model):
    time = models.CharField(max_length=300)
    latitude = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
    longitude = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )  
   #  accuracy = models.IntegerField()
    code = models.IntegerField()
    power = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
    node = models.IntegerField(blank=True,null=True)
    technology = models.CharField(max_length=50,blank=True,null=True)
    arfcn = models.IntegerField(blank=True,null=True)
    plmnId = models.IntegerField(blank=True,null=True)
    lac = models.IntegerField(blank=True,null=True)
    color = models.CharField(max_length=100,blank=True,null=True)
    cellId = models.BigIntegerField(blank=True,null=True)
    scan = models.CharField(max_length=50,blank=True,null=True)
    quality = models.DecimalField(
         max_digits=8, decimal_places=3,blank=True,null=True
      )
    
class Ranges(models.Model):
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
class Color_Info(models.Model):

      parameter = models.CharField(max_length=100,blank=True,null=True)
      name = models.CharField(max_length=100)
      count =models.IntegerField()
      color_range =  models.OneToOneField("Ranges",on_delete=models.CASCADE)
      distance = models.IntegerField()
      distribution = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
class Static_Info(models.Model):
   parameter = models.CharField(max_length=100,blank=True,null=True)
   count = models.IntegerField()
   mean = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
   max = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
   min = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
   median = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
   mode = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
   std = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
   variance = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
   ci_min = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )
   ci_max = models.DecimalField(
         max_digits=8, decimal_places=2,blank=True,null=True
      )


