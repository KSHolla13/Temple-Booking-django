from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class user_table(AbstractUser,PermissionsMixin):
    full_name=models.CharField(max_length=200,null=True,blank=True)
    username = models.CharField(max_length=50, blank=False, null=True,verbose_name="user name")
    phone_no=models.CharField(max_length=13,null=True,blank=True)
    email = models.EmailField(_('email address'), unique=True,blank=True,null=True)
    address=models.TextField(null=True,blank=True)
    pincode=models.CharField(max_length=6,null=True,blank=True)
    dob=models.DateField(max_length=10,null=True,blank=True)
    nakshatra=models.CharField(max_length=200,null=True,blank=True)
    rashi=models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name","username",'phone_no']   
    def __str__(self):
        return str(self.email)    


class sevas_table(models.Model):
    seva_name=models.CharField(max_length=200,null=True,blank=True)
    seva_description=models.TextField(null=True,blank=True)
    amount=models.CharField(max_length=100,null=True,blank=True)
    is_mahaseva=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return str(self.seva_name)    

 

class booking_table(models.Model):
    booking_id=models.CharField(max_length=100,null=True,blank=True)
    seva=models.ForeignKey(sevas_table,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(user_table,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    pincode=models.IntegerField(null=True,blank=True)
    nakshatra=models.CharField(max_length=200,null=True,blank=True)
    date=models.DateField(max_length=10,null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)
    razorpay_orderid=models.CharField(null=True,blank=True,max_length=100)
    payment=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)


class transaction_table(models.Model):
    razorpay_orderid=models.CharField(null=True,blank=True,max_length=100)
    razorpay_transactionid=models.CharField(null=True,blank=True,max_length=100)
    seva=models.ForeignKey(sevas_table,on_delete=models.CASCADE,null=True,blank=True)
    amount=models.CharField(max_length=10,null=True,blank=True)
    payment_type=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)
    user=models.ForeignKey(user_table,on_delete=models.CASCADE,null=True,blank=True)
    booking=models.ForeignKey(booking_table,on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)


class god_table(models.Model):
    lord_image = models.FileField(upload_to='godPhotos',null=True,blank=True)  
    description = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)


class festival_table(models.Model):
    name = models.CharField(max_length=400,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    photo = models.FileField(upload_to='festival',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)

class donation_table(models.Model): 
    pass


class shashvathaPooje_table(models.Model):
    pass 