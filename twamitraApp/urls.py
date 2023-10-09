from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("servicepage",views.servicepage,name="servicepage"),
]
