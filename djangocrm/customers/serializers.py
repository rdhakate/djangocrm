from rest_framework import serializers
from .models import Customer, CustomerEmail, CustomerPhone, CustomerAddress, CustomerWebsite

class CustomerEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerEmail
        fields = ['id', 'email']

class CustomerPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPhone
        fields = ['id', 'phone_number']

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ['id', 'address_line', 'city', 'postal_code', 'country']

class CustomerWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerWebsite
        fields = ['id', 'url']

class CustomerSerializer(serializers.ModelSerializer):
    emails = CustomerEmailSerializer(many=True, read_only=True)
    phones = CustomerPhoneSerializer(many=True, read_only=True)
    addresses = CustomerAddressSerializer(many=True, read_only=True)
    websites = CustomerWebsiteSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'description', 'created_at', 'emails', 'phones', 'addresses', 'websites']
