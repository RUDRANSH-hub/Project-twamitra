from django.db import models

# Create your models here.
class Professions(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

class CorporateDB(models.Model):
    cid = models.CharField(max_length=7, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    businessName = models.CharField(max_length=255)
    profession = models.ForeignKey(Professions,on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    referralCode = models.CharField(max_length=8,null=True)
    razorpay_order_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    has_paid = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name
    
class CorporatePayments(models.Model):
    cid = models.ForeignKey(CorporateDB,on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255)
    razorpay_signature = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.cid.name
    
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
    