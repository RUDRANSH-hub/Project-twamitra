from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(ModelForm):
    class Meta:
        model = CorporateDB
        fields = ['companyName', 'experience', 'address', 'pan','alternatePhone', 'signature','profilePic']
        
        