from django.db import models
import datetime
from django.conf import settings

# Create your models here.


class DriverTable(models.Model):
    name = models.CharField(max_length=500,default='',blank=True)
    taxi_number = models.CharField(max_length=500,default='',blank=True)
    balance = models.IntegerField(default=0,blank=True)
    is_rent_deducted_today = models.BooleanField(default=False)
    is_paid_today = models.BooleanField(default=False)
    last_rent_deduction_date = models.DateField( default=datetime.date.today)
    last_paid_date = models.DateField( default=datetime.date.today,)

    
    
    def __str__(self):
        return  f"{self.name} - {self.taxi_number}"
    