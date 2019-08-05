from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls

from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('condensed', views.condensed, name = "condensed"),
    path('create/', views.create, name = "create"),
    path('delete/<int:num>/', views.delete, name = "delete"),
    path('update/<int:num>/', views.update, name = "update"),
    path('activation/<int:num>/', views.activation, name = "activation"),
    path('status/<int:num>/<str:stat>/', views.status, name = "status"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name = "register"),
    path('pastprojects', views.pastprojects, name = "pastprojects"),
    path('offtrack', views.offtrack, name = "offtrack"),
    path('onwatch', views.onwatch, name = "onwatch"),
    path('myprojects', views.myprojects, name = "myprojects"),
    path('projectstatus/<int:num>/', views.projectstatus, name = "projectstatus"),



]
