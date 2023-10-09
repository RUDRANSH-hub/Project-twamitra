from django.contrib import admin

# Register your models here.
from account.models import account
@admin.register(account)
class account_detail(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')