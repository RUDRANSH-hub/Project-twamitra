from django.shortcuts import render, redirect
from .models import LoanApplication

# Create your views here.


def index(request):
    return render(request, "home.html")


def loan(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        loan_type = request.POST.get('loan_type')
        monthly_salary = request.POST.get('monthly_salary')
        loan_amount = request.POST.get('loan_amount')

        # Create a new LoanApplication object and save it
        application = LoanApplication(
            name=name,
            email=email,
            address=address,
            pincode=pincode,
            phone=phone,
            loan_type=loan_type,
            monthly_salary=monthly_salary,
            loan_amount=loan_amount
        )
        application.save()
        return redirect("")

    return render(request, "loanForm/loanForm.html")


# def submit_loan_application(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         pincode = request.POST.get('pincode')
#         phone = request.POST.get('phone')
#         loan_type = request.POST.get('loan_type')
#         monthly_salary = request.POST.get('monthly_salary')
#         loan_amount = request.POST.get('loan_amount')

#         # Create a new LoanApplication object and save it
#         application = LoanApplication(
#             name=name,
#             email=email,
#             address=address,
#             pincode=pincode,
#             phone=phone,
#             loan_type=loan_type,
#             monthly_salary=monthly_salary,
#             loan_amount=loan_amount
#         )
#         application.save()

#         # Optionally, redirect to a success page
#         return redirect('')

#     return render(request, 'loan_application_form.html')
