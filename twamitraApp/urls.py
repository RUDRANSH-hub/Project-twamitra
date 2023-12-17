from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("corporate-registration/", views.corporateRegistration, name="corporate-registration"),
    path("save_generated_code/", views.GenerateCode, name="codegeneration"),
    path("servicepage/",views.servicepage,name="servicepage"),
    path("payment-handler/",views.paymenthandler,name="paymenthandler"),
    path("carLoan/",views.carLoan,name="carLoan"),
    path("personalLoan/",views.personalLoan,name="personalLoan"),
    path("homeLoan/",views.homeLoan,name="homeLoan"),
    path("educationLoan/",views.educationLoan,name="educationLoan"),
    path("usedCarLoan/",views.usedCarLoan,name="usedCarLoan"),
    path("twoWheelerLoan/",views.twoWheelerLoan,name="twoWheelerLoan"),
    path("consultantServices/",views.consultantServices,name="consultantServices"),
    ]
