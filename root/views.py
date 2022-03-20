from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout






 



# Create your views here.
@login_required(login_url='/login')
def index(request):
    context = {'title':"Driver Listing"}
    available_drivers = DriverTable.objects.all()
    
    
    
    today_date = datetime.now(). strftime("%m/%d/%Y")
    context['today_date'] = today_date
    context['available_drivers'] = available_drivers
    return render(request, 'root/index.html',context)

 
def edit_driver(request,id=None):
    if request.method=="POST":
        name = request.POST['name']
        taxi_number = request.POST['taxi_number']
        balance = request.POST['balance']
        required_driver = None
        if id:
            required_driver = DriverTable.objects.get(id=id)
        else:
            required_driver = DriverTable()
    
        required_driver.name = name
        required_driver.taxi_number = taxi_number
        required_driver.balance = balance
        required_driver.save()
        return redirect("/")
    
    
    
    context = {'title':"Edit Driver Data" if id else "Add Driver"} 
    required_driver = DriverTable.objects.filter(id=id)
    if required_driver:
        required_driver = required_driver.first()
    context['required_driver'] = required_driver
    today_date = datetime.now(). strftime("%m/%d/%Y")
    context['today_date'] = today_date
    
    print(required_driver)
    
    
    return render(request, 'root/edit_driver.html',context)

 
 
 
def delete_driver(request,id):
    required_driver = DriverTable.objects.filter(id=id)
    required_driver.delete() 
    print(required_driver, " deleted !")
    return redirect("/")
    
 
@csrf_exempt
def pay_driver(request):
    id = int(request.POST['id'])
    payment_date = request.POST['payment_date']
    payment_date = datetime.strptime(payment_date, '%m/%d/%Y').date()

    
    
    
    paid_amount = int(request.POST['paid_amount'])
    required_driver = DriverTable.objects.get(id=id)
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
    
    required_driver = DriverTable.objects.get(id=id)
    required_driver.balance = required_driver.balance - rent
    required_driver.last_rent_deduction_date = payment_date
    required_driver.save()
    return JsonResponse({"balance":int(required_driver.balance)})
    