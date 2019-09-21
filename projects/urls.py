from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls

from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('create/', views.create, name = "create"),
    path('complete/<int:num>/', views.complete, name = "complete"),
    path('update/<int:num>/', views.update, name = "update"),
    path('activation/<int:num>/', views.activation, name = "activation"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name = "register"),
    path('pastprojects', views.pastprojects, name = "pastprojects"),
    path('projectstatus/<int:num>/', views.projectstatus, name = "projectstatus"),
    path('myprojects/', views.myprojects, name = "myprojects"),
    path('planner/', views.planner, name = "planner"),
    path('printable/', views.printable, name = "printable"),
    path('thisweek/', views.thisweek, name = "thisweek"),
    path('ontrack/', views.ontrack, name = "ontrack"),
    path('offtrack/', views.offtrack, name = "offtrack"),
    path('onwatch/', views.onwatch, name = "onwatch"),
    path('milestonecomplete/', views.milestonecomplete, name = "milestonecomplete")
]
