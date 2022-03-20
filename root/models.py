from django.db import models
import datetime
from django.conf import settings
from pytz import timezone 
from datetime import  datetime
from  django.utils.timezone import  now
# Create your models here.


class DriverTable(models.Model):
    name = models.CharField(max_length=500,default='',blank=True)
    taxi_number = models.CharField(max_length=500,default='',blank=True)
    balance = models.FloatField(default=0,blank=True)
    owed = models.FloatField(default=0,blank=True)
    is_rent_deducted_today = models.BooleanField(default=False)
    is_paid_today = models.BooleanField(default=False)
    last_rent_deduction_date = models.DateField( null=True,blank=True,default=now)
    last_paid_date = models.DateField(null=True,blank=True,default=now)
    
    

    
    
    def __str__(self):
        return  f"{self.name} - {self.taxi_number}"
    