from django.urls import path
from scan_result import views
urlpatterns = [

    path("cell_result_table/", views.Scan_result_cell),
    path("cell_result_neighbor/", views.Scan_result_neighbor),
    path("power_pie_chart/",views.PowerPieChart),
    path("quality_pie_chart/",views.QualityPieChart)
    
    
    
]
