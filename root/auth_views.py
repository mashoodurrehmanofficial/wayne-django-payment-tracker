from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout








def login_page(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            print("login successful !") 
            return redirect('index') 
        else:
            return render(request, 'login.html',{"error":"Sorry, Email or password is incorrect !","page_title":"Login"})
      
         
    context = {"page_title":"Login"}      
    today_date = datetime.now(timezone(settings.TIME_ZONE)). strftime("%m/%d/%Y")
    context['today_date'] = today_date
    return render(request, 'root/login_page.html', context)


def logout_page(request):
    logout(request)
    return redirect('login_page')
