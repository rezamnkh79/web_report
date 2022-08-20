from django.contrib import admin
from django.urls import path
from map import views
urlpatterns = [

    # path('login/',views.login),

    path('map/',views.Map),
    path('insert/',views.set_color_info),
    path('data/',views.Data),
    path('test/ping/map',views.PingTest),
    path('test/qoe',views.QoE),
    path('rsrp/',views.RSRP),
    path('rssi/',views.RSSI),
    path('setting/',views.setting),
    path('line/',views.test_line_chart),
    path('circle/',views.test_circle_chart),
    path('temp/',views.InsertARFNTable),
    path('technology/',views.Technology),
    path('arfcn/',views.ARFCN),
    path('code/',views.Code),
    path('dns/',views.DNS),
    path("qoe/",views.QoE),
    path('update/',views.update_points),
    path("redis",views.Redis),
    path("updates/", views.update, name="update"),
    path("static/", views.insert_static_info, name="static")
    
    
]
