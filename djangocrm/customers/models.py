from django.db import models
from crmapp.models import Company

class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class CustomerEmail(models.Model):
    customer = models.ForeignKey(Customer, related_name='emails', on_delete=models.CASCADE)
    email = models.EmailField()

class CustomerPhone(models.Model):
    customer = models.ForeignKey(Customer, related_name='phones', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, related_name='addresses', on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

class CustomerWebsite(models.Model):
    customer = models.ForeignKey(Customer, related_name='websites', on_delete=models.CASCADE)
    url = models.URLField()
