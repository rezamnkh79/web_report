from django.urls import path
from procedures import views

urlpatterns = [
    path('messages/', views.MessageCounter),
    # path('dns/',views.DNS),
    # path("qoe/",views.QoE),
    # path("downlink/",views.DownLink),
]
