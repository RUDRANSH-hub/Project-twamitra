from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name =  models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=15,null=True)
    is_customer = models.BooleanField(default=False)
    is_corporate = models.BooleanField(default=False)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email


# class CorporateDB(AbstractUser):
#     cid = models.CharField(max_length=7, primary_key=True, unique=True)
#     name = models.CharField(max_length=255)
#     businessName = models.CharField(max_length=255)
#     profession = models.ForeignKey(Professions,on_delete=models.CASCADE)
#     email = models.EmailField(unique=True, null=True)
#     phone = models.CharField(max_length=15)
#     location = models.CharField(max_length=255)
#     referralCode = models.CharField(max_length=8,null=True)
#     razorpay_order_id = models.CharField(max_length=255,null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     has_paid = models.BooleanField(default=False)
#     subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.SET_NULL,null=True)
#     active_till = models.DateField(auto_now_add=False)
#     is_active = models.BooleanField(default=False)
#     is_corporate = models.BooleanField(default=True)
        
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self) -> str:
#         return self.name
