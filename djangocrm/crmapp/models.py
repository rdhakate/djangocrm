from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

no_space_validator = RegexValidator(r'^\S+$', 'No spaces are allowed.')

# -- Company Model --
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscription_plan = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# -- Custom User Manager --
class UserManager(BaseUserManager):
    def create_user(self, company_name, email, password=None, **extra_fields):
        if not company_name or not email:
            raise ValueError("Company name and email are required")

        # 🚫 No spaces allowed in any of these
        if ' ' in company_name:
            raise ValueError("Company name must not contain spaces")
        if ' ' in email:
            raise ValueError("Email must not contain spaces")
        if password is not None and (' ' in password or password.strip() != password):
            raise ValueError("Password must not contain spaces")

        company_name = company_name.strip()
        email = self.normalize_email(email.strip())

        company, _ = Company.objects.get_or_create(name=company_name)

        user = self.model(company=company, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, company_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(company_name, email, password, **extra_fields)

# -- Custom User Model --
class User(AbstractBaseUser, PermissionsMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, validators=[no_space_validator])
    email = models.EmailField(unique=True, validators=[no_space_validator])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company']

    objects = UserManager()

    def __str__(self):
        return f'{self.email} ({self.company.name})'


# -- Customer Models --
class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
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


# -- Calendar/Activity Models --
class Activity(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.customer.name})"
