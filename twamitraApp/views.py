import random
from django.shortcuts import render
from django.shortcuts import render, redirect
from decimal import Decimal
from django.shortcuts import render
from .models import *
import uuid
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def index(request):
    return render(request, "home.html")

def corporateRegistration(request):
    context = {"professions": Professions.objects.all()}
    if request.method == 'POST':
        name = request.POST.get('name')
        businessName = request.POST.get('businessName')
        profession_name = request.POST.get('profession')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if(not name or not email or not phone or not businessName or not profession_name):
            return HttpResponseBadRequest()
        try:
            referralCode = request.POST.get('referralCode')
        except:
            referralCode = None
            
        disc = 0
        if referralCode:
            try:
                code_obj = GeneratedCode.objects.get(code=referralCode)
                if not code_obj.is_redeemed:
                    disc = int(code_obj.percentage.strip('%'))
                else:
                    disc = 0
                print(code_obj.percentage.strip('%'))
                print("*******************")
                print(disc)
            except GeneratedCode.DoesNotExist:
                disc = 0
        profession = Professions.objects.get(name=profession_name)
        profession_mapping = {
                'CA': 'C',
                'ARCHITECT/VALUER': 'E',
                'ADVOCATE/LEGAL ADVISOR': 'L',
                'DSA': 'D',
                'OTHERS': 'O',
            }
        profession_code = profession_mapping.get(profession.name, 'O')
        random_number = str(random.randint(1, 9999)).zfill(4)
        generated_id = f'C{random_number}{profession_code}{name[0]}'
        while CorporateDB.objects.filter(cid=generated_id).exists():
            random_number = str(random.randint(1, 9999)).zfill(4)
            generated_id = f'C{random_number}{profession_code}{name[0]}'
        
        amount = (25000-((25000*disc)/100))*100
        currency = 'INR'
        data = { "amount": amount, "currency": "INR"}
        razorpay_order = razorpay_client.order.create(data=data)

        razorpay_order_id = razorpay_order['id']
        callback_url = 'http://127.0.0.1:8000/payment-handler/'
 
        context = {"professions": Professions.objects.all()}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = "INR"
        context['callback_url'] = callback_url
        corporate = CorporateDB.objects.create(
            cid=generated_id,
            name=name,
            businessName=businessName,
            profession=profession,
            email=email,
            phone=phone,
            referralCode=referralCode,
            razorpay_order_id = razorpay_order_id
        )
        return render(request, "confirmPayment.html",context)
    else:
        return render(request, "corporateRegistration.html",context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            razorpay_signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            corporate = CorporateDB.objects.get(razorpay_order_id = razorpay_order_id)
            server_order_id = corporate.razorpay_order_id
            result = razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
            })
            print("################################-")
            print(result)
            if result:
                corporate.has_paid = True
                corporate.save()
                CorporatePayments.objects.create(
                cid=corporate,
                razorpay_order_id = razorpay_order_id,
                razorpay_payment_id = razorpay_payment_id,
                razorpay_signature = razorpay_signature
                )
                if corporate.referralCode is not None:
                    code_obj = GeneratedCode.objects.get(code = corporate.referralCode)
                    code_obj.is_redeemed = True
                    code_obj.save()
            return render(request,'home.html')           
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()



def GenerateCode(request):
    if request.method == 'POST' and request.user.is_superuser:
        code = request.POST.get('code')
        percentage = request.POST.get('percentage')
        GeneratedCode.objects.create(code=code, percentage=percentage)
        print("Created Successfully",code)
        return redirect('codegeneration')
    
    if request.user.is_superuser:
        unique_code = str(uuid.uuid4())[:8]
        return render(request, "generatecode.html", {'unique_code': unique_code})
    else:
        return render(request, "Error.html")
    

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

