from django.db import models

class LoanApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    LOAN_CHOICES = [
        ('personal', 'Personal Loan'),
        ('home', 'Home Loan'),
        ('car', 'Car Loan'),
        ('business', 'Business Loan'),
    ]
    loan_type = models.CharField(max_length=20,choices=LOAN_CHOICES)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name
