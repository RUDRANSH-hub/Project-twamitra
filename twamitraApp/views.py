from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "home.html")



def signup(request):
    return render(request, "signup.html")


