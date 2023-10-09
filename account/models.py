from django.db import models

# Create your models here.
class account(models.Model):
    username = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)
    
    def __str__(self):
        return self.username + self.email
    


