from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('travian/add_building/', views.add_building, name='add_building'),
    path('travian/build_building/', views.build_building, name='build_building'),
    path('travian/upgrade_building/', views.upgrade_building, name='upgrade_building'),
]
