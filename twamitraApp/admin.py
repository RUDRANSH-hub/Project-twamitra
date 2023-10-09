from django.contrib import admin

# Register your models here.
from twamitraApp.models import loan_detail
@admin.register(loan_detail)
class load_details(admin.ModelAdmin):
    list_display = ('name', 'email', 'loan_type', 'loan_amount')  # Customize the fields displayed in the admin list view
