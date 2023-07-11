from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import random
from django.contrib.auth import authenticate, login 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from siteflow.mixins import *
from django.contrib.auth import logout
from siteflow.models import *
from django.http import JsonResponse

# Create your views here.
  
class customerEmailThread(threading.Thread): 
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.emailfrom=settings.EMAIL_HOST_USER
        self.recipient_list = recipient_list
        # self.html_content = html_content
        threading.Thread.__init__(self)
    def run (self):
        try:
            msg=EmailMultiAlternatives(
                    self.subject,
                    self.message,
                    self.emailfrom,
                    self.recipient_list,
                    )
            msg.attach_alternative( self.message, "text/html")
            a=msg.send()
            print("------------------",a)
        except Exception as e:          
            pass


class user_registration(View):
    template_name = 'customer/register.html'
    def get(self,request,*args,**kwargs):
        
        return render(request,self.template_name) 
    def post(self,request,*args,**kwargs):
        print(request.POST)
        fullname=request.POST.get("fullname")   
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        user=user_table.objects.filter(email=email)         
        if user.exists():
            messages.info(request,"Email already Registered, Please login")
        else:
            if password1==password2:
                try:
                    otp = random.randint(1000,9999)
                    request.session['otp'] = otp
                    request.session['email'] = email
                    request.session['phone'] = phone
                    request.session['fullname'] = fullname
                    request.session['password'] = make_password(password2)
                    # messages.success(request,"Enter the OTP")
                    subject="Forgot Password OTP"
                    message=f"{otp} is your OTP, Don't share this otp with anyone"
                    customerEmailThread(subject,message,[email]).start()
                    messages.info(request,"otp sent to email")
                    return redirect("userOtp")
                except Exception as e:
                    messages.info(request,"Please Enter Valid Email id")
            else:
                messages.error(request,"Password didn't match")
        return redirect("Custregistration") 



class registration_otp(View):
    template_name = 'customer/userOtp.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 
    def post(self,request,*args,**kwargs):
        otp=request.POST.get("otp") 
        print(otp)
        print(type(otp))
        otpp=request.session.get("otp") 
        print(otpp)
        if int(otp)==int(otpp): 
            fullname=request.session.get("fullname") 
            email=request.session.get("email")
            phone=request.session.get("phone")
            password=request.session.get("password")
            user=user_table.objects.filter(email=email)
            if user.exists()==False:
                user_table.objects.create(full_name=fullname,email=email,password=password,phone_no=phone)#creating the customer using fullname,email,password and is_vendor false because registering as customer
                if fullname!=None:  
                    del request.session["fullname"]
                if email!=None:
                    del request.session["email"]
                if password!=None:
                    del request.session["password"]
                if otpp!=None:
                    del request.session["otp"]
                if phone!=None:
                    del request.session["phone"]
                messages.success(request,"Registered Successfully")
                return redirect("login")
            else:
                messages.info(request,"Email already Registered Please login")
                return redirect("login")
        else:
            messages.error(request,"Invalid OTP")
            return redirect("userOtp")


class user_login(View):
    template_name = 'customer/login.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 
    def post(self,request,*args,**kwargs):  
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email,password)
        try:
            user=user_table.objects.filter(email=email)
            print(user)
            if user.exists():
                authuser=authenticate(request,username=email,password=password)   
                print(authuser)     
                if authuser is not None:
                    login(request,authuser)
                    messages.success(request,"Logged in Successfully")
                    return redirect("dashboard")
                else:
                    messages.error(request,"Invalid Credentials")
                    return redirect("login")
            else:
                messages.error(request,"Invalid Credentials")
                return redirect("login")
        except Exception as e:        
           messages.error(request,"Invalid Credentials")
           return redirect("login")


# class userForgotPassword(View):
#     template_name = 'customer/forgotPassword.html'
#     def get(self,request,*args,**kwargs):  
#         otp=request.session.get("forgototp")
#         email=request.session.get("f_email")
#         print(otp,email)
#         return render(request,self.template_name)
#     def post(self,request,*args,**kwargs):
#         if request.POST.get("action")=="sendotp":
#             print(request.POST)
#             try:
#                 email=request.POST.get("email")
#                 user_table.objects.get(email=email)
#                 otp = random.randint(1000,9999)
#                 print(otp)
#                 request.session['forgototp'] = otp
#                 subject="Forgot Password OTP"
#                 message=f"{otp} is your OTP, Don't share this otp with anyone"
#                 customerEmailThread(subject,message,[email]).start()
#                 messages.info(request,"otp sent to email")
#                 return JsonResponse({"message":True})
#             except Exception as e:
#                 return JsonResponse({"message":False,"res":"Please Enter Valid Email id"})
#         elif request.POST.get("action")=="verifyotp":
#             print(request.POST)
#             otp=request.POST.get("otp")
#             email=request.POST.get("email")
#             s_otp=request.session.get("forgototp")
#             request.session['f_email']=email
#             print(request.session.get('f_email'))

#             print(s_otp,otp)
#             if str(s_otp)==str(otp):
#                 return JsonResponse({"message":True,"res":"OTP Verified"})
#             else:
#                 return JsonResponse({"message":False,"res":"Invalid OTP"})
            
#         elif request.POST.get("action")=="changepassword":    
#             print(request.POST)        
#             email=request.session.get('f_email')
#             print(email)
#             password1=request.POST.get("password1")
#             password2=request.POST.get("password2")
#             print(password2)
#             if password1==password2:
#                 user=user_table.objects.get(email=email)
#                 user.password=make_password(password2)
                
#                 return JsonResponse({"message":True,"user":user})               
#             else:
#                 return JsonResponse({"message":False})

class userForgotPassword(View):
    template_name="customer/forgotPassword.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    def post(self,request,*args,**kwargs):
        print(request.POST.get("email"))
        email=request.POST.get("email")
        user=user_table.objects.filter(email=email)
        print("------------------",request.POST)
        if user.exists():
            action=request.POST.get("action")
            if action=="send":
                otp = random.randint(1000,9999)
                subject="Forgot OTP"
                request.session['otp'] = otp
                message=f"{otp} is your OTP for Forgot Password\n" 
                customerEmailThread(subject, message, [email]).start()
                return JsonResponse({"message":True,"message2":"OTP sent to your provided email address, Please don't refresh the page"})
            elif action=="otp":
                otp=request.POST.get("otp")
                otp1=request.session.get("otp")
                print("-----------",otp1)
                if str(otp)==str(otp1):
                    if otp1!=None:
                        del request.session["otp"]
                    return JsonResponse({"message":True,"message2":"OTP Verified, Please provide new password"})
                else:
                    return JsonResponse({"message":False,"message2":"Invalid OTP"})
            elif action=="final":
                password=request.POST.get("password")
                password2=request.POST.get("cpassword")
                if password==password2:
                    user.update(password=make_password(password2))
                    return JsonResponse({"message":True,"message2":"Password Changed Successfully"})
                else:
                    return JsonResponse({"message":False,"message2":"Password didn't match"})
        else:
            return JsonResponse({"message":False,"message2":"Account doesn't exists, check provided email address again"})    
class dashboard(LoginRequiredMixin,View):
    template_name='customer/dashboard.html'
    def get(self,request,*args,**kwargs):
        bookings = booking_table.objects.select_related("seva").filter(user=request.user)
        user = request.user
        context={
            'bookings':bookings[::-1],
            'user':user
        }
        return render(request,self.template_name,context)
                      
def logout_request(request):
    logout(request)
    return redirect("/")

# class custForgotpassOTPVerify(View):
#     template_name = 'customer_app/customer_forgotpassotp.html'
#     def get(self,request,*args,**kwargs):
#         return render(request,self.template_name)
#     def post(self,request,*args,**kwargs):
#         otp=request.POST.get("otp")
#         forgototp=request.session.get("forgototp")
#         if otp==forgototp:
#             password=request.session.get("fpassword")
#             email=request.session.get("f_email")
#             user_table.objects.filter(email=email).update(password=make_password(password))
#             if email!=None:
#                 del request.session['f_email']
#             if password!=None:
#                 request.session['fpassword']
#             if forgototp!=None:
#                 request.session['forgototp']
#             messages.success(request,"Password Updated Successfully")
#             return redirect("Custlogin")
#         else:
#             messages.error(request,"Invalid OTP")
#             return redirect("custforgot-otp")        
# user.objects.create(full_name=fullname,email=email,password=make_password(password2),is_vendor=False,phone_no=phone)#creating the customer using fullname,email,password and is_vendor false because registering as customer        
#         messages.success(request,"Registered Successfully")
#         return redirect("Custlogin")


#------------------------------------end1-------------------------------------

