from django.urls import path

from core import views

urlpatterns = [
    path('', views.SankeyView.as_view(), name='sankey'),
    path('map', views.MapView.as_view(), name='map'),
]
