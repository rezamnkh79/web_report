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
    path('rsrq/',views.RSRQ),
    path('setting/',views.setting),
    path('line/',views.test_line_chart),
    path('circle/',views.test_circle_chart),
    path("plmn_id/", views.PLMN_Id),
    path('temp/',views.InsertARFNTable),
    path('technology/',views.Technology),
    path('arfcn/',views.ARFCN),
    path('code/',views.Code),
    path("arfcn_code/",views.ARFCN_Code ),
    path("cell_id/", views.Cell_Id),
    path('dns/',views.DNS),
    path("qoe/",views.QoE),
    path("downlink/",views.DownLink),
    path("cell_result_table/", views.Scan_result_cell),
    path("cell_result_neighbor/", views.Scan_result_neighbor),
    path('update/',views.update_points),
    path("redis",views.Redis),
    path("updates/", views.update, name="update"),
    path("static/", views.insert_static_info, name="static"),
    path("table/", views.insert_table_result),
    path("readpoints/",views.ReadPointInfoData),
    path("readcolor/",views.ReadColorInfoData),
    path("readtest/",views.ReadTestTableData),
    path("readstatic/",views.ReadStaticData),
    path("readrange/",views.ReadRangeData),
    path("power_pie_chart/",views.PowerPieChart),
    path("quality_pie_chart/",views.QualityPieChart)
    
    
    
]
