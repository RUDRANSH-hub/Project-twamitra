from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate , login
from  account.models import account
from django.contrib import messages

# Create your views here.
def registeruser(request):
    
    if request.method == "POST":
      username = request.POST.get("username",None)
      email = request.POST.get("email",None)
      password = request.POST.get("password",None)
      try:
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        account( username= username, email=email, password= password ).save()
        login(request,user)
      except:
        messages.success(request, " Username already Taken! Try With another Username...")
        return render( request, "registeruser.html", {"username":username, "email":email})
      
      return redirect ("/auth/dashboard")
      
    return render( request, "registeruser.html")

def loginuser(request):
 if request.method=="POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
  
      user = authenticate(username=username, password=password)

      if user is not None:
        login(request, user)
        return redirect ("/auth/dashboard")
               
      else:
        messages.success(request, "Incorrect Credentials! Please check your Details and Retry...")
        return render(request, "loginuser.html", {"username": username})
    
 return render( request, "loginuser.html")


def logoutuser(request):
     logout(request)
     return render ( request, "logoutuser.html")


def dashboard(request):
   return render ( request, "dashboard.html")
