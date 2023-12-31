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
    path("subServices/<str:sub>/",views.subServices,name="subServices"),
    path("corporateDashboard/",views.corporateDashboard,name="corporateDashboard"),
    path("corporateLogin/",views.corporateLogin,name="corporateLogin"),
    path("corporateLogout/",views.corporateLogout,name="corporateLogout"),
    path("checkReferralCode/<str:referralCode>/",views.checkReferralCode,name="checkReferralCode"),
    path("verifyReferralCode/", views.verifyReferralCode,name="verifyReferralCode"),
    path("initiatePaymentRequest/",views.initiatePaymentRequest,name="initiatePaymentRequest"),
    path("corporateProfileForm/",views.corporateProfileForm,name="corporateProfileForm"),
    path("viewProviders/",views.viewProviders,name="viewProviders"),
]
