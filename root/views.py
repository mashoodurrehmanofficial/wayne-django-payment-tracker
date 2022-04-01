from time import timezone
import pytz
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from pytz import timezone 
from .emailSender import send_email
from django.contrib.auth.models import User


def synchronizeDriverOwedAmount():
    available_drivers = Profile.objects.all()
    for driver in available_drivers:
        # print("-"*10)
        pre_owned_amount = 0
        today_date = datetime.now(timezone(settings.TIME_ZONE)).date()
        # if driver.last_rent_deduction_date == today_date:
        pre_owned_amount = driver.temp_owed 
            
        last_rent_deduction_date = driver.last_rent_deduction_date 
        days = (today_date - last_rent_deduction_date).days
         
        
        if datetime.now(timezone(settings.TIME_ZONE)).hour<=18:
            days = days-1
        
        print("days = ", days)
        
        if days<0:
            days=0
            print("days = ", days)
        
        owed_amount = pre_owned_amount + (int(days)*60)
        driver.owed = owed_amount
        driver.save()
    pass
        # print(days)
 



# Create your views here.
@login_required(login_url='/login')
def index(request,delinquent_drivers=None):
    context = {'title':"Driver Listing"} 
    available_drivers = Profile.objects.all()
    
    synchronizeDriverOwedAmount()
         
        
        
    
    available_drivers = Profile.objects.filter(user__is_superuser=False)
    
    if delinquent_drivers:
        available_drivers = available_drivers.filter(owed__gte=0)
    
    
    
    today_date = datetime.now(timezone(settings.TIME_ZONE)). strftime("%m/%d/%Y")
    context['today_date'] = today_date
    context['available_drivers'] = available_drivers
    context['profile'] = Profile.objects.get(user=request.user)
    
    
    
    
    return render(request, 'root/index.html',context)

 
def edit_driver(request,id=None):
    
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        taxi_number = request.POST['taxi_number']
        balance = request.POST['balance']
        owed = request.POST['owed']
        required_driver = None
        if id:
            required_driver = Profile.objects.get(id=id)
            required_user = required_driver.user
        else:
            required_driver = Profile()
            required_user = User()
    
        
    
        required_user.username = name
        required_user.email = email
        required_user.set_password(password)
        required_user.save()
        
        required_driver = Profile.objects.get(user=required_user)
    
        required_driver.password = password
        required_driver.taxi_number = taxi_number
        required_driver.balance = balance
        required_driver.owed = owed
        required_driver.verified = True
        required_driver.save()
        
        print("owed = ", required_driver.owed)
        
        return redirect("/")
    
    
    
    context = {'title':"Edit Driver Data" if id else "Add Driver"} 
    synchronizeDriverOwedAmount()
    
    required_driver = Profile.objects.filter(id=id)
    if required_driver:
        required_driver = required_driver.first()
    context['required_driver'] = required_driver 
    today_date = datetime.now(timezone(settings.TIME_ZONE)). strftime("%m/%d/%Y")
    context['today_date'] = today_date
    
     
    
    now_time = datetime.now(timezone(settings.TIME_ZONE)). strftime("%m/%d/%Y")
    
    print(now_time)
    
    
    return render(request, 'root/edit_driver.html',context)

 
 
 
def delete_driver(request,id):
    required_driver = Profile.objects.filter(id=id)
    if required_driver:
        
        required_user = required_driver.first().user
        required_user.delete()
        
    required_driver.delete() 
    print(required_driver, " deleted !")
    return redirect("/")
    
 
@csrf_exempt
def pay_driver(request):
    id = int(request.POST['id'])
    payment_date = request.POST['payment_date']
    payment_date = datetime.strptime(payment_date, '%m/%d/%Y').date()

    
    
    
    paid_amount = int(request.POST['paid_amount'])
    required_driver = Profile.objects.get(id=id)
    required_driver.balance = required_driver.balance + paid_amount
    required_driver.last_paid_date = payment_date
    required_driver.save()
    
    
    
    print("-"*50)
    print(payment_date== required_driver.last_paid_date)
    print(required_driver.last_paid_date)
    print("-"*50)
    
    return JsonResponse({"balance":int(required_driver.balance)})
    
    
 
@csrf_exempt
def deduct_rent(request):
    id = int(request.POST['id'])
    rent = int(request.POST['rent'])
    payment_date = request.POST['payment_date']
    payment_date = datetime.strptime(payment_date, '%m/%d/%Y').date()
    
    required_driver = Profile.objects.get(id=id) 
    required_driver.owed = required_driver.owed - rent
    required_driver.temp_owed = required_driver.temp_owed - rent
    
    if required_driver.owed <0:
        required_driver.owed = 0
    
    if required_driver.temp_owed <0:
        required_driver.temp_owed = 0
    
    required_driver.last_rent_deduction_date = payment_date
    required_driver.save()
    return JsonResponse({"balance":int(required_driver.balance)})
    