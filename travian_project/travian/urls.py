from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('travian/add_building/', views.add_building, name='add_building'),
    path('travian/build_resource/', views.build_building, name='build_resource'),
    path('travian/upgrade_building/', views.upgrade_building, name='upgrade_building'),
    path('travian/build_infrastructure', views.build_infrastructure, name='build_infrastructure'),
    path('travian/infantry/', views.build_infantry, name='build_infantry'),
    path('travian/troop_building/', views.troop_building, name='troop_building'),
]
