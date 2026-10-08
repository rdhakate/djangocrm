"""
URL configuration for crmapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customers.views import CustomerViewSet
from calendar_app.views import ActivityViewSet
from crmapp.views import MultiTenantLoginView
from crmapp.views import MultiTenantRegisterView
from crmapp.views import UserProfileView
from crmapp.views import LogoutView
from crmapp.views import login_page
from crmapp.views import dashboard_page
from crmapp.views import profile_page
from crmapp.views import CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # for browsable API login/logout
    path('api/login/', MultiTenantLoginView.as_view(), name='multi_tenant_login'),
    path('api/register/', MultiTenantRegisterView.as_view(), name='multi_tenant_register'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    #Jwt Tokens
    path('api/token/', TokenObtainPairView.as_view(), name='jwt_token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='jwt_token_verify'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('login/', login_page, name='login'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('profile/', profile_page, name='profile'),

    
]
