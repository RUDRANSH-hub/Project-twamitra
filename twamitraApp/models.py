from django.db import models

# Create your models here.
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