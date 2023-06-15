from django.urls import path
from . import views
from user_profile.views import signup
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.base, name='base'),
]
