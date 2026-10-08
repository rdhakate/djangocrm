from django import forms

class TenantLoginForm(forms.Form):
    company_name = forms.CharField(max_length=255)
    user_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
