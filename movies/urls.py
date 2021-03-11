# Router
# Základní směrovač celé aplikace
# Stará se o to, že když přijde požadavek, má ho poslat na určité místo

from django.contrib import admin
from django.urls import path
from movies import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topten', views.topten, name='topten'),
]

