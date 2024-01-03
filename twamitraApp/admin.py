from django.contrib import admin
from twamitraApp.models import *

# Register your models here.
@admin.register(loan_detail)
class load_details(admin.ModelAdmin):
    list_display = ('name', 'email', 'loan_type', 'loan_amount')  # Customize the fields displayed in the admin list view

admin.site.register(GeneratedCode)
admin.site.register(Professions)
admin.site.register(CorporateDB)
admin.site.register(CorporatePayments)
admin.site.register(ServiceType)
admin.site.register(SubscriptionType)
admin.site.register(AppointmentPayment)
admin.site.register(CorporateAppointment)


