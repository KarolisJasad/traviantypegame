from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from user_profile.views import signup

urlpatterns = [
    path('', signup, name='signup'),
    path('village/creation', views.village_creation, name='village_creation'),
    path('home/', views.home, name='home'),
    path('travian/build_resource/', views.build_building, name='build_resource'),
    path('travian/upgrade_building/', views.upgrade_building, name='upgrade_building'),
    path('travian/build_infrastructure', views.build_infrastructure, name='build_infrastructure'),
    path('travian/infantry/', views.build_infantry, name='build_infantry'),
    path('travian/troop_building/', views.troop_building, name='troop_building'),
    path('travian/player_list', views.player_list, name='player_list'),
    path('attack/<int:player_id>/', views.attack_view, name='attack'),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +  
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
