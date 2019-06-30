from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls

from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('projectcards/', views.projectcards, name = "projectcards"),
    path('myprojects/', views.myprojects, name = "myprojects"),
    path('create/', views.create, name = "create"),
    path('switch/', views.switch, name = "switch"),
    path('update/<int:num>/', views.update, name = "update"),
    path('delete/<int:num>/', views.delete, name = "delete"),
    path('milestonecomplete/', views.milestonescomplete, name = "milestonecomplete"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name = "register"),


]
