from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from crmapp.models import Company, User
from django.contrib.auth import get_user_model

User = get_user_model()

class MultiTenantRegisterSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)

    def validate_company_name(self, value):
        try:
            if ' ' in value:
                    raise serializers.ValidationError("Company name must not contain spaces")   
            company = Company.objects.get(name=value)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Company does not exist")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        company = Company.objects.get(name=validated_data['company_name'])
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            company=company
        )
        return user
    
class MultiTenantLoginSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        company_name = attrs.get('company_name')
        email = attrs.get('email')
        password = attrs.get('password')

        # Validate company
        try:
            company = Company.objects.get(name=company_name)
        except Company.DoesNotExist:
            raise serializers.ValidationError('Invalid company.')

        # Authenticate user manually with multi-tenant logic
        try:
            user = User.objects.get(company=company, email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        if not user.is_active:
            raise serializers.ValidationError({'email': 'This account is inactive.'})

        attrs['user'] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_active']  # Add more fields if needed
        read_only_fields = ['email']  # Email is usually not editable

class CustomTokenObtainPairSerializerold(TokenObtainPairSerializer):
    company_name = serializers.CharField(write_only=True)

    def validate(self, attrs):
        company_name = attrs.pop('company_name', None)
        email = attrs.get('email')
        password = attrs.get('password')

        # Validate presence
        if not company_name:
            raise serializers.ValidationError({'company_name': 'Company name is required.'})
        if not email:
            raise serializers.ValidationError({'email': 'Email is required.'})
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})

        # Check if the company exists
        try:
            company = Company.objects.get(name__iexact=company_name)
        except Company.DoesNotExist:
            raise serializers.ValidationError({'company_name': 'Invalid company name.'})

        # Check if a user with this email exists in this company
        try:
            user = User.objects.get(email__iexact=email, company=company)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'No user found with this email under this company.'})

        # Check password
        if not user.check_password(password):
            raise serializers.ValidationError({'password': 'Incorrect password.'})

        if not user.is_active:
            raise serializers.ValidationError({'email': 'This account is inactive.'})

        self.user = user
        return super().validate(attrs)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    company_name = serializers.CharField(write_only=True)

    def validate(self, attrs):
        company_name = attrs.pop('company_name', None)
        email = attrs.get('email')
        password = attrs.get('password')

        if not company_name:
            raise serializers.ValidationError({'company_name': 'Company name is required.'})
        if not email:
            raise serializers.ValidationError({'email': 'Email is required.'})
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})

        try:
            # 🚨 One query: match user by email AND company name together
            user = User.objects.select_related('company').get(
                email__iexact=email,
                company__name__iexact=company_name
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'detail': 'Invalid login. Please check company name, email, and password.'
            })

        if not user.check_password(password):
            raise serializers.ValidationError({'password': 'Incorrect password.'})

        if not user.is_active:
            raise serializers.ValidationError({'email': 'This account is inactive.'})

        self.user = user
        return super().validate(attrs)