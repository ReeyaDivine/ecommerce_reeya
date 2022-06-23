from django.contrib import admin
from .models import PaymentGateway

class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ["token", "balance", "expiry_date", "is_active",]
    
    class Meta:
     model = PaymentGateway

admin.site.register(PaymentGateway, PaymentGatewayAdmin)
