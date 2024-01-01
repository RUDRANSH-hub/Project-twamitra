import random
from django.shortcuts import render, redirect
from decimal import Decimal
from .models import *
from .forms import ProfileForm
import uuid
from datetime import datetime, timedelta
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib import messages
from django.contrib.auth import logout, authenticate , login
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import is_corporate_user


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
        location = request.POST.get('location')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if(not name or not email or not phone or not businessName or not profession_name or not location or not password1 or not password2):
            messages.success(request, "Enter all the fields")
            return render( request, "corporateRegistration.html")                
        if(password1 != password2):
            messages.success(request, "Password mismatch!")
            return render( request, "corporateRegistration.html")                
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
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=email, name=name, phone=phone, email=email,password=password1,is_corporate=True)
                corporate = CorporateDB.objects.create(                
                    user=user,
                    cid=generated_id,
                    businessName=businessName,
                    profession=profession,
                    location=location,
                    is_active=False
                )
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        except Exception as e:
            print(e)
            messages.success(request, " Username already Taken! Try With another Username...")
            return render( request, "corporateRegistration.html", context)
        return redirect ('corporateDashboard')
    else:
        return render(request, "corporateRegistration.html",context)

# @user_passes_test(is_corporate_user)
@login_required(login_url='/corporateLogin/')
def corporateDashboard(request):
    user = User.objects.get(email=request.user.email)
    corporate = CorporateDB.objects.get(user=user)
    services = ServiceType.objects.filter(profession=corporate.profession)
    # if corporate["has_paid"] == False:
    #     corporate["cid"] == "*******"
    print(services)
    context = {'user': user, 'corporate': corporate,'services': services}
    return render(request, "corporateDashboard.html", context)


def checkReferralCode(request, referralCode):
    code = referralCode
    try:
        referralCode = GeneratedCode.objects.get(code=code)
    except GeneratedCode.DoesNotExist:
        return JsonResponse({"status": False, "message": "Code not found!"})
    
    if referralCode.is_redeemed:
        return JsonResponse({"status": False, "message": "Code already redeemed!"})
    else:
        return JsonResponse({"status": True, "message": "Verified!"})

@login_required(login_url='/corporateLogin/')
def corporateProfileForm(request):
    corporate_db = CorporateDB.objects.get(user=request.user)
    if request.method == 'POST':

        print("dfcgvhbjnkfcvgbhnjmkgvbhnj ********************************")
        company_name = request.POST.get('companyName')
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        pan = request.POST.get('pan')
        alternate_phone = request.POST.get('alternatePhone')

        corporate_db.companyName = company_name
        corporate_db.experience = experience
        corporate_db.address = address
        corporate_db.pan = pan
        corporate_db.alternatePhone = alternate_phone

        corporate_db.profilePic = request.FILES.get('profilePic')
        corporate_db.signature = request.FILES.get('signature')

        corporate_db.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('corporateDashboard')
    else:
        data = {
        'companyName': corporate_db.companyName,
        'experience': corporate_db.experience,
        'address': corporate_db.address,
        'pan': corporate_db.pan,
        'alternatePhone': corporate_db.alternatePhone,
        'signature': corporate_db.signature,
        'profilePic': corporate_db.profilePic
        }

        print("gadbad")
    return render(request, 'corporateProfile.html', {'data': data})

def corporateLogin(request):
    if request.user.is_authenticated and request.user.is_corporate:
        return redirect('corporateDashboard')
    
    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        try:
            corporate = User.objects.get(email=email)
            if corporate.is_corporate == False:
                messages.error(request, "Unauthorized access!")
                return redirect('corporateLogin')
        except:
            messages.add_message(request, messages.INFO, "User does not exist")
            print("User does not exist")
            return render(request, 'corporateLogin.html')
        user = authenticate(request, email = email, password = password)    
        
        if user is not None and user.is_corporate:
            login(request, user)
            print("logged in")
            return redirect('corporateDashboard')
        else:
            messages.error(request,  "Invalid credentials")
            
    return render(request,'corporateLogin.html')



def corporateLogout(request):
  logout(request)
  return redirect('home')

# @login_required(login_url="corporateLogin")
def verifyReferralCode(request):
    print("******IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII ****")
    if request.method == 'POST'and request.user.is_corporate:
        try:
            referralCode = request.POST.get('referralCode')
        except:
            referralCode = None
        print(referralCode)    
        disc = 0
        if referralCode is not None:
            try:
                code_obj = GeneratedCode.objects.get(code=referralCode)
                if not code_obj.is_redeemed:
                    disc = int(code_obj.percentage.strip('%'))
                else:
                    disc = 0
            except GeneratedCode.DoesNotExist:
                disc = 0
        print("********************************")
        print(disc)
        
        discount = True if disc != 0 else False
        subscriptions = SubscriptionType.objects.all().values()
        print(subscriptions)
        if discount:
            for subscription in subscriptions:
                subscription["new_price"] = subscription["default_price"]-((subscription["default_price"]*disc)/100)
        print(subscriptions)        
        print("tebsdkcbsvkjsvsdbljvndl")
        print(type(referralCode))
        context = {"discount": discount, "discount_percentage": 1000, "subscriptions": subscriptions, "referralCode":referralCode}       
        return render(request,"chooseSubscription.html",context)
    return HttpResponseBadRequest("Invalid request")
        
def initiatePaymentRequest(request):
    if request.method == 'POST' and request.user.is_corporate:
        user = request.user
        corporate = CorporateDB.objects.get(user=user)
        amount = request.POST.get('default_price')
        value = request.POST.get('value')
        referralCode = request.POST.get('referralCode')
        if referralCode == 'None':
            referralCode = None
        print("above all")
        print(request.POST.get('referralCode'))
        print(type(request.POST.get('referralCode')))
        
        print(amount, value, referralCode)
        print(type(amount), type(referralCode), type(value))
        try:
            subType = SubscriptionType.objects.get(value=value)
        except:                        
            messages.error(request,  "Something went wrong!")
        print(subType)
        print(type(None))
        print(type(referralCode))
        
        amount = int(float(amount))*100
        currency = 'INR'
        data = { "amount": amount, "currency": currency}
        razorpay_order = razorpay_client.order.create(data=data)

        razorpay_order_id = razorpay_order['id']
        callback_url = 'http://127.0.0.1:8000/payment-handler/'
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = "INR"
        context['callback_url'] = callback_url
        
        if referralCode is not None:
            print("im ahehbcdjbcsv svlnlvnxvlknk")
            referCode = GeneratedCode.objects.get(code=referralCode)
            referCode.is_redeemed = True
            referCode.save()
        paymentObj = CorporatePayments.objects.create(
            amount = amount,
            cid=corporate,
            subscription_type = subType,
            referralCode=referralCode,
            razorpay_order_id = razorpay_order_id
        )
        return render(request, "confirmPayment.html",context)

# def corporateRegistration(request):
#     context = {"professions": Professions.objects.all()}
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         businessName = request.POST.get('businessName')
#         profession_name = request.POST.get('profession')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         if(not name or not email or not phone or not businessName or not profession_name):
#             return HttpResponseBadRequest()
#         try:
#             referralCode = request.POST.get('referralCode')
#         except:
#             referralCode = None
            
#         disc = 0
#         if referralCode is not None:
#             try:
#                 code_obj = GeneratedCode.objects.get(code=referralCode)
#                 if not code_obj.is_redeemed:
#                     disc = int(code_obj.percentage.strip('%'))
#                 else:
#                     disc = 0
#             except GeneratedCode.DoesNotExist:
#                 disc = 0
#         profession = Professions.objects.get(name=profession_name)
#         profession_mapping = {
#                 'CA': 'C',
#                 'ARCHITECT/VALUER': 'E',
#                 'ADVOCATE/LEGAL ADVISOR': 'L',
#                 'DSA': 'D',
#                 'OTHERS': 'O',
#             }
#         profession_code = profession_mapping.get(profession.name, 'O')
#         random_number = str(random.randint(1, 9999)).zfill(4)
#         generated_id = f'C{random_number}{profession_code}{name[0]}'
#         while CorporateDB.objects.filter(cid=generated_id).exists():
#             random_number = str(random.randint(1, 9999)).zfill(4)
#             generated_id = f'C{random_number}{profession_code}{name[0]}'
        
#         amount = (25000-((25000*disc)/100))*100
#         currency = 'INR'
#         data = { "amount": amount, "currency": "INR"}
#         razorpay_order = razorpay_client.order.create(data=data)

#         razorpay_order_id = razorpay_order['id']
#         callback_url = 'http://127.0.0.1:8000/payment-handler/'
#         context = {"professions": Professions.objects.all()}
#         context['razorpay_order_id'] = razorpay_order_id
#         context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#         context['razorpay_amount'] = amount
#         context['currency'] = "INR"
#         context['callback_url'] = callback_url
#         corporate = CorporateDB.objects.create(
#             cid=generated_id,
#             name=name,
#             businessName=businessName,
#             profession=profession,
#             email=email,
#             phone=phone,
#             referralCode=referralCode,
#             razorpay_order_id = razorpay_order_id
#         )
#         return render(request, "confirmPayment.html",context)
#     else:
#         return render(request, "corporateRegistration.html",context)





@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
            razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            razorpay_signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            paymentObject = CorporatePayments.objects.get(razorpay_order_id = razorpay_order_id)
            corporate = paymentObject.cid
            # server_order_id = corporate.razorpay_order_id
            result = razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
            })
            if result is True:
                corporate.has_paid = True
                corporate.is_active = True
                noOfDays = int(paymentObject.subscription_type.value) * 30
                current_date = datetime.now().date()
                endDate = current_date + timedelta(days=noOfDays)
                corporate.active_till = endDate
                corporate.subscription_type = paymentObject.subscription_type
                corporate.save()
                paymentObject.razorpay_order_id = razorpay_order_id,
                paymentObject.razorpay_payment_id = razorpay_payment_id,
                paymentObject.razorpay_signature = razorpay_signature
                paymentObject.verified = True
                if paymentObject.referralCode is not None and not paymentObject.referralCode == '':
                    try:
                        paymentObject.referralUsed = True
                        code_obj = GeneratedCode.objects.get(code = corporate.referralCode)
                        code_obj.is_redeemed = True
                        code_obj.save()
                    except Exception as e:
                        print("Error",e)
                paymentObject.save()
            return redirect('corporateDashboard')          
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

def personalLoan(request):
    return render(request, "loanForms/personalLoanForm.html")

def educationLoan(request):
    return render(request, "loanForms/educationLoanForm.html")
def homeLoan(request):
    return render(request, "loanForms/homeLoanForm.html")

def twoWheelerLoan(request):
    return render(request, "loanForms/twoWheelerLoanForm.html")

def carLoan(request):
    return render(request, "loanForms/carLoanForm.html")

def usedCarLoan(request):
    return render(request, "loanForms/usedCarLoanForm.html")

def consultantServices(request):
    return render(request, "consultantServices.html")

def subServices(request,sub):
    profession = Professions.objects.get(name=sub)
    services = ServiceType.objects.filter(profession=profession)
    return render(request, "subServices.html", {"services":services, "profession":profession})

def viewProviders(request):
    if request.method == 'GET':
        service_name = request.GET.get('service_name')
        service_price = request.GET.get('service_price')
        service = ServiceType.objects.get(name=service_name)
        profession = Professions.objects.get(name=service.profession)
        corporates = CorporateDB.objects.filter(profession=profession)
        return render(request, 'viewProviders.html', {"corporates": corporates ,'service': service})

