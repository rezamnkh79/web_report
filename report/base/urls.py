from django.urls import path
from base import views

urlpatterns = [
    path('info/', views.GeneralInfo),
    path('speed/', views.SpeedInfo),
    # path("qoe/",views.QoE),
    # path("downlink/",views.DownLink),
]
