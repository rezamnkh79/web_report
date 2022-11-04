from django.contrib import admin
from .models import Point_Info,Ranges,Color_Info, Region,Static_Info, Table,Result_Table
# Register your models here.
admin.site.register(Point_Info)
admin.site.register(Ranges)
admin.site.register(Color_Info)
admin.site.register(Static_Info)
admin.site.register(Region)
admin.site.register(Table)
admin.site.register(Result_Table)