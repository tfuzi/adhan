from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.index , name='index'),
    path('home/' , views.index , name='home'),
    path('get_hijri/' , views.get_hijri , name='get_hijri'),
    path('get_timings/' , views.get_timings , name='get_timings'),
    path('get_lat_lon/', views.get_lat_lon, name='get_lat_lon'),
    path('setting/' , views.setting , name='setting'),
    path('get_data/' , views.get_data , name='get_data'),
    path('get_random_hadith/' , views.get_random_hadith , name='get_random_hadith'),
    path('get_city_country/' , views.get_city_country , name='get_city_country'),
]
