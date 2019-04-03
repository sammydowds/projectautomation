from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls

from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('create/', views.create, name = "create"),
    path('switch/', views.switch, name = "switch"),
    path('update/<int:num>/', views.update, name = "update"),
    path('close/<int:num>/', views.close, name = "close"),
    path('dashboard/<int:num>/', views.dashboard, name = "dashboard"),
    path('milestonecomplete/', views.milestonescomplete, name = "milestonecomplete"),
    path('capacity/', views.capacity, name = "capacity"),
    path('suggested/<int:num>/', views.suggested, name = "suggested"),
    path('tasks/', views.tasks, name = "tasks"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name = "register")

]
