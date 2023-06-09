from django.urls import path
from .views import *
 
urlpatterns = [
 
    path('home/',HomeView,name='home'),
    path('signup/',RegisterView,name='signup'),
    path('',SigninView,name='signin'),

    path('logout/', logoutView, name='logout'),
    path('otp/', OtpVerifyView, name='otp'),
 
]
