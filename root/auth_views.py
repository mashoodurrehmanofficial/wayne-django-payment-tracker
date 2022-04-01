from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
import uuid
from .emailSender import  send_email



def getDomain(request):
    return request.build_absolute_uri('/')[:-1] 


def login_page(request):  
    if request.method=='POST':
        email = request.POST['email']
        
        required_user_record = User.objects.filter(email=email)
        if required_user_record: 
            required_user_record = required_user_record.first()
            username = required_user_record.username
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                print("login successful !") 
                return redirect('index') 
        else:
            print("Login error")
            return render(request, 'root/login_page.html',{"error":"Sorry, Email or password is incorrect !","page_title":"Login"})

    context = {"page_title":"Login"}       
    return render(request, 'root/login_page.html', context)



def register_page(request):
    context = {"page_title":"Register"}       
    if request.method=='POST':
        email = request.POST['email']
        taxi_number = request.POST['taxi_number']
        username = request.POST['username']
        password = request.POST['password'] 
        required_profile = Profile.objects.filter(user__email=email,verified=True) 
        if required_profile:
            print(required_profile)
            context['error'] = "Email Already Exists !"
         
        else:
            required_user = User.objects.filter(email=email)
            if required_user:
                required_user = required_user.first()
            else:
                required_user = User(username=username)
                required_user.set_password(password)
                required_user.email = email
                required_user.save()
                
            required_profile = Profile.objects.filter(user=required_user)
            required_profile = required_profile.first() if required_profile.exists() else Profile()
            required_profile.user = required_user
            required_profile.password = password
            required_profile.taxi_number = taxi_number
            required_profile.auth_code = str(uuid.uuid4())
            required_profile.save()
            
            
            print(required_profile, "--", required_profile.auth_code)
            
            send_email(
                recipient=email,
                subject="Verify Account",
                body=f"{getDomain(request)}/verify_email_account/{required_profile.auth_code}"
            )
            
            
            print("send token")
            print("new account")
            
            return render(request, 'root/register_page.html',{"message":"Verification link has been sent to your email","page_title":"Register"})

    return render(request, 'root/register_page.html', context)




def verifyEmailAccount(request,auth_code):
    required_profile = Profile.objects.filter(auth_code=auth_code)
    context = {"page_title":"Login",}       
    if required_profile:
        print(auth_code)
        required_profile=required_profile.first() 
        required_profile.verified =True
        required_profile.auth_code =""
        required_profile.save()
        context[ "message"] = "Account verified !"
    else:
        context[ "error"] = "Invalid Auth Token"
        
    return render(request, 'root/login_page.html', context)




def sendPasswordResetLink(request):
    context = {"page_title":"Register"}       
    if request.method=='POST':
        email = request.POST['email']
        required_profile = Profile.objects.filter(user__email=email)
        if required_profile:
            required_profile = required_profile.first()
            required_profile.password_reset_code = str(uuid.uuid4())
            required_profile.save() 
            send_email(
                recipient=email,
                subject="Reset Password",
                body=f"{getDomain(request)}/password_reset_form/{required_profile.password_reset_code}"
            )
        context["message"] = "Password Reset Link sent successfully !"

        
        
        print(required_profile)
        
    return render(request, 'root/send_password_reset_link_form.html', context)




def passwordResetForm(request,password_reset_code): 
    context = {"page_title":"Reset Password"}     
    if request.method=='POST':
        password = request.POST['password']
        required_user  = User.objects.filter(profile__password_reset_code=password_reset_code)
        if required_user:
            required_user = required_user.first()
            required_user.set_password(password)
            required_profile = Profile.objects.get(user=required_user)
            required_profile.password_reset_code = password_reset_code
            required_profile.password = password
            required_profile.verified = True
            required_profile.save()
            required_user.save()
            return render(request, 'root/login_page.html',{"message":"Password updated successfully !","page_title":"Login"})
        
        print(required_user)
    
    context['password_reset_code'] = password_reset_code
      
    return render(request, 'root/password_reset_form.html', context)




def change_password(request): 
    context = {"page_title":"Reset Password"}     
    if request.method=='POST':
        password = request.POST['password']
        required_user  = request.user
        required_user.set_password(password)
        required_user.save()
        user = authenticate(username=required_user.username,password=password)
        if user is not None:
            login(request, user)   
            return redirect("/")     

  
  
      
    return render(request, 'root/change_password.html', context)








def resendEmailVerificationLink(request):
    pass


def logout_page(request):
    logout(request)
    return redirect('login_page')
