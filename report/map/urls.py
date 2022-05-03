from django.contrib import admin
from django.urls import path
from map import views
urlpatterns = [

    # path('login/',views.login),

    path('map/',views.Map),
    path('insert/',views.Insert_info),
    path('data/',views.Data),
    path('test/',views.test),
    path('rsrp/',views.RSRP),
    path('setting/',views.setting),
    path('line/',views.test_line_chart),
    
]
