from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("corporate-registration", views.corporateRegistration, name="corporate-registration"),
    path("save_generated_code", views.GenerateCode, name="codegeneration"),
    path("servicepage",views.servicepage,name="servicepage"),
]
