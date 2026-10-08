from django.contrib import admin
from crmapp.models import Customer, CustomerEmail, CustomerPhone, CustomerAddress, CustomerWebsite

admin.site.register(Customer)
admin.site.register(CustomerEmail)
admin.site.register(CustomerPhone)
admin.site.register(CustomerAddress)
admin.site.register(CustomerWebsite)
