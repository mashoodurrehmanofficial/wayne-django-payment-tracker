from django.db import models
import datetime
from django.conf import settings
from pytz import timezone 
from datetime import  datetime
from  django.utils.timezone import  now
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


# Create your models here.


class Profile(models.Model): 
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    taxi_number = models.CharField(max_length=500,default='',blank=True)
    password = models.CharField(max_length=500,default='',blank=True)
    
    auth_code = models.CharField(max_length=500,default='',blank=True)
    password_reset_code = models.CharField(max_length=500,default='',blank=True)
    verified = models.BooleanField(default=False)
    
    balance = models.FloatField(default=0,blank=True)
    owed = models.FloatField(default=0,blank=True)
    is_rent_deducted_today = models.BooleanField(default=False)
    is_paid_today = models.BooleanField(default=False)
    last_rent_deduction_date = models.DateField( null=True,blank=True,default=now)
    last_paid_date = models.DateField(null=True,blank=True,default=now)
    
    def __str__(self):
        return  f"{self.user} - {self.taxi_number}"


# method for updating
@receiver(post_save, sender=User, dispatch_uid="update_stock_count")
def update_stock(sender, instance, **kwargs):
    if not Profile.objects.filter(user=instance).exists():
        Profile(user=instance).save()
        print("---", instance)

    # instance.save()