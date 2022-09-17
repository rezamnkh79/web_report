from django.contrib import admin
from django.urls import path
from map import views
urlpatterns = [

    # path('login/',views.login),

    path('',views.Map),

    path('rsrp/',views.RSRP),
    path('rssi/',views.RSSI),
    path('rsrq/',views.RSRQ),
    path('line/',views.test_line_chart),
    path('tech_pie_chart/',views.TechPieChart),
    path("plmn_id/", views.PLMN_Id),
    path('temp/',views.InsertARFNTable),
    path('technology/',views.Technology),
    path('arfcn/',views.ARFCN),
    path('code/',views.Code),
    path("arfcn_code/",views.ARFCN_Code ),
    path("cell_id/", views.Cell_Id),
    path("lac/",views.LAC)
    # path('update/',views.update_points),
    # path("redis",views.Redis),
    # path("updates/", views.update, name="update"),
    # path("static/", views.insert_static_info, name="static"),
    # path("table/", views.insert_table_result),
    # path("readpoints/",views.ReadPointInfoData),
    # path("readcolor/",views.ReadColorInfoData),
    # path("readtest/",views.ReadTestTableData),
    # path("readstatic/",views.ReadStaticData),
    # path("readrange/",views.ReadRangeData),
    
]
