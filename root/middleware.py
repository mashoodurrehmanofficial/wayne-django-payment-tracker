 
from tracemalloc import start 
from .models import *
from django.contrib.auth.models import User
from django.conf import settings
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
from django.contrib.auth import authenticate, login,logout 
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404,HttpResponseRedirect
from django.http import HttpResponse,HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin

from django.urls import reverse

def context_processor(request):   
    context = {}
    today_date = datetime.now(timezone(settings.TIME_ZONE)). strftime("%m/%d/%Y")
    context['today_date'] = today_date
    current_absolute_url = str(request.build_absolute_uri())
    current_child_url = request.META.get('PATH_INFO', None)
    current_child_url = current_child_url[1:] if str(current_child_url).startswith('/') else current_child_url
    
 
    
     
    
    
    
    
    
    
    
    
    
    return context











class CustomMiddleware(MiddlewareMixin):
    
    def _init_(self, get_response):
        self.get_response = get_response

    # Code that is executed in each request before the view is called
    def _call_(self, request):
        response = self.get_response(request)
        

        
        # Code that is executed in each request after the view is called
        return response
 
 
 
    # This code is executed if an exception is raised
    def process_request(self, request):
        pass
        # print("incoming url = ",incoming_url)
        # incoming_url = request.build_absolute_uri()
        # if  'dashboard' in incoming_url  or 'login' in incoming_url or  'bussiness_admin' in incoming_url: 
        #     if manageOtp(request): 
        #         print("---> ACCOUNT LOCKED !") 
        #         return HttpResponsePermanentRedirect(f"{settings.DOMAIN}accounts/authotp")

        #     required_user = request.user 
        #     if 'bussiness_admin' in incoming_url and not  required_user.is_superuser and required_user.is_authenticated:
        #         logout(request)
        #         return redirect("bussiness_admin/pwzg")
        #     elif 'login' in incoming_url and required_user.is_superuser and required_user.is_authenticated:
        #         print(incoming_url, "-->",required_user.is_superuser)
        #         logout(request)
        #         return redirect("login_register")
        
 

 