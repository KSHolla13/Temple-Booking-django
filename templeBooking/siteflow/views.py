from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import razorpay
from django.conf import settings
# Create your views here.


class home(View):
    template_name='siteflow/home.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 
    
class sevas(View):
    template_name='siteflow/sevas.html'
    def get(self,request,*args,**kwargs):
        nityaSevas=sevas_table.objects.filter(is_mahaseva=False)
        mahaSevas=sevas_table.objects.filter(is_mahaseva=True)
        context={
            "n":nityaSevas,
            "m":mahaSevas
        }
        return render(request,self.template_name, context) 

class sevaDetails(LoginRequiredMixin,View):
    template_name='siteflow/sevaBookView.html'
    def get(self,request,slug,*args,**kwargs):
        Seva=sevas_table.objects.get(id=int(slug)) 
        c = {"Seva":Seva }             
        return render(request,self.template_name,c)     
    def post(self,request,*args,**kwargs):
        name=request.POST.get("name")  
        date=request.POST.get("date")
        nakshatra=request.POST.get("nakshatra")
        pincode=request.POST.get("pincode")
        address=request.POST.get("address")
        idd=request.POST.get("idd")
        print('---------------------------------'+address)
        seva=sevas_table.objects.get(id=int(idd))
        if name!='' and date!='' and pincode!='' and address!='':
            booking_table.objects.create(user=request.user,name=name,date=date,nakshatra=nakshatra,pincode=pincode,address=address,seva=seva)
            messages.success(request,"booking creatwd makwe payment")

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            # Create a Razorpay order
            order_data = {
                'amount': int(seva.amount)*100,
                'currency': 'INR', 
                # Add other order details as per your requirements
            }
            order = client.order.create(data=order_data)

            # Get the Razorpay order ID
            order_id = order['id']
            context={
                'order_id': order_id,
                'razorpay_key':settings.RAZOR_KEY_ID,
                'amount':seva.amount,
                "Seva":seva 
                }
            # Render the payment template with Razorpay order ID
            return render(request, self.template_name, context)
            # return redirect("razorpay",slug=slug)
        else:
            messages.error(request,"invalid booking") 
            return redirect('/')   
        

class aboutTemple(View):
    template_name='siteflow/aboutTemple.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 

class calender(View):
    template_name='siteflow/calender.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 

class festivals(View):
    template_name='siteflow/festivals.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)     

class gallery(View):
    template_name='siteflow/gallery.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)  

class eHundi(View):
    template_name='siteflow/eHundi.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)             