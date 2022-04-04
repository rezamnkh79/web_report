
from statistics import mode
from django.db import models

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
   color = models.CharField(max_length=200)



# class Point(models.Model):
#     location = models.ListCharField(base_field=models.CharField())
    