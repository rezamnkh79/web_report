from django.contrib import admin
from .models import Point_Info,Ranges,Color_Info,Static_Info
# Register your models here.
admin.site.register(Point_Info)
admin.site.register(Ranges)
admin.site.register(Color_Info)
admin.site.register(Static_Info)