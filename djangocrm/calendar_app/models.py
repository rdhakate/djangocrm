from django.db import models
from crmapp.models import Company
from customers.models import Customer

class Activity(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='activities')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.customer.name})"
