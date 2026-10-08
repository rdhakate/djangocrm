from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import TenantLoginForm
from .models import Company, User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import generics, permissions

from .serializers import UserProfileSerializer
from .serializers import MultiTenantLoginSerializer, MultiTenantRegisterSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from crmapp.serializers import CustomTokenObtainPairSerializer

#Multi tenant login view
class MultiTenantLoginView(APIView):
    permission_classes = []  # Allow unauthenticated access

    def post(self, request):
        serializer = MultiTenantLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Multi tenant Register view
class MultiTenantRegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = MultiTenantRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def tenant_login_view(request):
    form = TenantLoginForm(request.POST or None)
    message = ''
    if request.method == 'POST' and form.is_valid():
        company_name = form.cleaned_data['company_name']
        user_email = form.cleaned_data['user_email']
        password = form.cleaned_data['password']

        try:
            company = Company.objects.get(name=company_name)
            user = User.objects.get(email=user_email, company=company)
            if user.check_password(password):
                login(request, user)
                return redirect('dashboard')  # You can update this route
            else:
                message = 'Invalid credentials'
        except (Company.DoesNotExist, User.DoesNotExist):
            message = 'Invalid company or email'
    return render(request, 'login.html', {'form': form, 'message': message})

#User profile view
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

#Logout view and blacklist the url    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Will raise if blacklist app not set up
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def login_page(request):
    return render(request, "login.html")

def dashboard_page(request):
    return render(request, "dashboard.html")

def profile_page(request):
    return render(request, "profile.html")
