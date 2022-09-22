from django.urls import path
from tests import views
urlpatterns = [
    path('ping',views.PingTest),
    path('dns/',views.DNS),
    path("qoe/",views.QoE),
    path("downlink/",views.DownLink),  
]
