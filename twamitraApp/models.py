from django.db import models
from django.contrib.auth.models import AbstractUser
from accountApp.models import User

# Create your models here.
class SubscriptionType(models.Model):
    type = models.CharField(max_length=20)
    value = models.PositiveIntegerField()
    default_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.type
    
class Professions(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

def user_profile_pic_path(instance, filename):
    return f'Images/corporates/profile/user_{instance.cid}-{filename}'

def user_signature_path(instance, filename):
    return f'Images/corporates/signature/user_{instance.cid}-{filename}'


class CorporateDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cid = models.CharField(max_length=7, unique=True)
    businessName = models.CharField(max_length=255)
    profession = models.ForeignKey(Professions,on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    companyName = models.CharField(max_length=255,null=True)
    experience = models.CharField(max_length=255,null=True)
    address = models.TextField(null=True)
    pan = models.CharField(max_length=20,null=True)
    alternatePhone = models.CharField(max_length=15,null=True)
    profilePic = models.ImageField(upload_to=user_profile_pic_path,null=True)
    signature = models.ImageField(upload_to=user_signature_path,null=True)
    has_paid = models.BooleanField(default=False)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.SET_NULL,null=True)
    active_till = models.DateField(auto_now_add=False,null=True)
    is_active = models.BooleanField(default=False)
        
    def __str__(self) -> str:
        return self.user.name

class CorporatePayments(models.Model):
    cid = models.ForeignKey(CorporateDB,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.SET_NULL,null=True)
    referralUsed = models.BooleanField(default=False)
    referralCode = models.CharField(max_length=8,null=True)
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255,null=True)
    razorpay_signature = models.CharField(max_length=255,null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.cid.user.name} - {self.subscription_type} - {self.amount}'
    
class loan_detail(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    loan_type = models.CharField(max_length=20, choices=[
        ('personal', 'Personal Loan'),
        ('home', 'Home Loan'),
        ('car', 'Car Loan'),
        # Add more options as needed
    ])
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    year_salary=models.DecimalField(max_digits=10, decimal_places=2)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add more fields as needed

    def __str__(self):
        return self.name
    
class GeneratedCode(models.Model):
    code = models.CharField(max_length=8, unique=True, null=False)
    PERCENTAGE_CHOICES = [
        ('25', '25'),
        ('50', '50'),
        ('75', '75'),
        ('100', '100'),
    ]
    percentage = models.CharField(max_length=20, choices=PERCENTAGE_CHOICES,null=False,default='25%')
    is_redeemed = models.BooleanField(default=False)
        
    def __str__(self):
        return self.code
    
class ServiceType(models.Model):
    name = models.CharField(max_length=150)
    profession = models.ForeignKey(Professions,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self) -> str:
        return f'{self.name} - {self.profession.name}'