from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name =  models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username + self.email


    


