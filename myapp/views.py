from django.shortcuts import render, redirect
from .form import UserCreateForm
from .models import OtpModel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import math, random
from django.conf import settings
from django.core.mail import send_mail


# for alpha nuemeric OTP 
def otp_provider():
    corpus= "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    generate_OTP = "" 
    size=7
    length = len(corpus) 
    for i in range(size) : 
        generate_OTP+= corpus[math.floor(random.random() * length)] 
    return generate_OTP

# Otp email sender 
def send_otp_in_mail(user,otp):
    subject = 'Otp for signin'
    message = f'Hi {user.email}, here we sent otp for secure login \n Otp is - {otp.otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["parthmehta724@gmail.com", ]
    send_mail(subject, message, email_from, recipient_list)

# User Signup
def RegisterView(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            usrname = form.cleaned_data['username']
            print(usrname)
            form.save()
            messages.success(request, f'{usrname} Successfully Registred')
            form = UserCreateForm()
        return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreateForm()
        context = {'form': form, }
    return render(request, 'signup.html', context)


# User Signin
def SigninView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        upass = request.POST.get('password')
        user = authenticate(email=email, password=upass)
        OtpModel.objects.filter(user=user).delete()
        print(user)
        if user is None:
            messages.error(request, 'Please Enter Correct Credinatial')
            return redirect('/')
        else:
            # login(request, user)
            messages.success(request, 'Please verify otp')
            otp_stuff = OtpModel.objects.create(user=user,otp=otp_provider())
            send_otp_in_mail(user,otp_stuff)
            return redirect('/otp/')
    else:
        if request.user.is_authenticated:
            return redirect('/home/')
        else:
            return render(request, 'signin.html')

def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, '🙋‍ You are Successfully Logged Out !')
        return redirect('/')
    else:
        messages.info(request, '☹︎ Please Login First')
    return redirect('/')


def HomeView(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        messages.info(request, '☹︎ Please Login First')
    return redirect('/')

def OtpVerifyView(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        verify_otp = OtpModel.objects.filter(otp=otp)
        if verify_otp.exists():
            login(request, verify_otp[0].user)
            return redirect('/home/')
        else:
            messages.error(request,"Invalid otp!")
            return redirect('/otp/')
    else:
        return render(request, 'otp.html')