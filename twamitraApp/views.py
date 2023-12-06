from django.shortcuts import render
from django.shortcuts import render, redirect
from twamitraApp.models import loan_detail# Create your views here.
from decimal import Decimal
def index(request):
    return render(request, "base.html")

from django.shortcuts import render
from .models import loan_detail  # Import your LoanDetail model here

def servicepage(request):
    if request.method == 'POST':
    # Retrieve data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        loan_type = request.POST.get('loan_type')
        
        # Convert monthly_salary to Decimal
        monthly_salary= request.POST.get('monthly_salary')
        # monthly_salary = Decimal(monthly_salary_str) if monthly_salary_str else Decimal('0.00')
        
        # Convert loan_amount to Decimal
        loan_amount = request.POST.get('loan_amount')
        # loan_amount = Decimal(loan_amount_str) if loan_amount_str else Decimal('0.00')
        
        # Calculate the annual salary
        try:
            monthly_salary = Decimal(monthly_salary)
            year_salary = monthly_salary * 12
        except Exception as e:
    # Handle the case where the provided monthly_salary is not a valid decimal
            year_salary = 0
        
        # print("appliocation start")
        
        # Create a new LoanDetail instance with the received data
        application = loan_detail(
            name=name,
            email=email,
            address=address,
            pincode=pincode,
            phone=phone,
            loan_type=loan_type,
            monthly_salary=monthly_salary,
            year_salary=year_salary,
            loan_amount=loan_amount,
        )


        try:
            application.save()  # Save the LoanDetail instance to the database
            
        except Exception as e:
            print(f"Error while saving data: {e}")
            # Handle the exception, perhaps return an error response

        
        return redirect ("/servicepage") # Redirect to a success page or URL
    return render(request, "loanForm/loanForm.html")
  ## currently adding loan only 

