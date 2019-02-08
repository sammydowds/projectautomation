from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('create/', views.create, name = "create"),
    path('switch/', views.switch, name = "switch"),
    path('update/<int:num>/', views.update, name = "update"),
    path('close/<int:num>/', views.close, name = "close"),
    path('dashboard/<int:num>/', views.dashboard, name = "dashboard"),
    path('milestonecomplete/', views.milestonescomplete, name = "milestonecomplete")


]
