from django.contrib import admin
from django.urls import path,include
from account import views
urlpatterns = [
    
    path("registeruser",views.registeruser,name="registeruser"),
    path("loginuser",views.loginuser,name="loginuser"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("logoutuser",views.logoutuser,name="logoutuser"),
]