"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from users.apps import UsersConfig
from users.views import (LoginView, UserListView, LogoutView, RegisterView, ProfileView,
                         SendConfirmView, EmailVerifyView, EmailErrorView,
                         PasswordView, set_active)


app_name = UsersConfig.name


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('', UserListView.as_view(), name='users'),
    path('<int:pk>/', set_active, name='set_active'),

    path('send_confirm/', SendConfirmView.as_view(), name='send_confirm'),
    path('send_confirm/error_page/', EmailErrorView.as_view(), name='email_error'),
    path('email_verify/<str:token>/', EmailVerifyView.as_view(), name='email_verify'),

    path('reset_password/', PasswordView.as_view(), name='reset_password'),
]
