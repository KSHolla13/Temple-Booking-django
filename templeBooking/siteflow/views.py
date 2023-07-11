from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import razorpay
from django.conf import settings
import shortuuid
from customer.views import customerEmailThread
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

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
        if request.POST.get("action")=="request":
            print(request.POST)
            name=request.POST.get("name")  
            date=request.POST.get("date")
            nakshatra=request.POST.get("nakshatra")
            pincode=request.POST.get("pincode")
            address=request.POST.get("address")
            idd=request.POST.get("idd")
            seva=sevas_table.objects.get(id=int(idd))
            if name and date and pincode and address:
                
                messages.success(request,"booking creatwd makwe payment")
                # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

                # Create a Razorpay order
                order_data = {
                    'amount': int(seva.amount)*100,
                    'currency': 'INR', 
                    # Add other order details as per your requirements
                }
                order = razorpay_client.order.create(data=order_data)
                
                # Get the Razorpay order ID
                order_id = order['id']
                s = shortuuid.ShortUUID(alphabet="0123456789")
                bid = s.random(length=5)
                booking_id="TS_"+str(bid)
                booking=booking_table.objects.create(user=request.user,name=name,date=date,nakshatra=nakshatra,pincode=pincode,address=address,seva=seva,razorpay_orderid=order_id,booking_id=booking_id)
                print("-------------------------",booking)
                callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/{}/{}'.format(request.user.email,seva.amount,booking.id,idd))
                context={
                    "status":True,
                    'order_id': order_id,
                    'razorpay_key':settings.RAZOR_KEY_ID,
                    'amount':seva.amount,
                    'address':address,
                    "pincode":pincode,
                    "name":name,
                    "callback_url":callback_url
                    # "Seva":seva 
                    }
                # Render the payment template with Razorpay order ID
                return JsonResponse(context)
                # return render(request, self.template_name, context)
                # return redirect("razorpay",slug=slug)
            else:
                messages.error(request,"invalid booking") 
                return redirect('/')  
         
        
@csrf_exempt
def paymenthandler(request,str,amount,booking_id,seva_id):
    # only accept POST request.
    originalamount=amount
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
           
            if result is not None:
                try:
                    # capture the payemt
                    # razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    # return render(request, 'paymentsuccess.html')
                    subject="Temple Seva Payment Successfull"
                    message1=f"Order id: {razorpay_order_id} \n Payment id: {payment_id} \n Amount: {originalamount} Thank You, your payment is successfull"
                    customerEmailThread(subject, message1, [str]).start()
                    user=user_table.objects.get(email=str)
                    seva=sevas_table.objects.get(id=int(seva_id))
                    booking=booking_table.objects.get(id=int(booking_id))
                    # orderstable.objects.create(user=user,orderid=razorpay_order_id,paymentid=payment_id,price=originalamount,productname=product)
                    # print("--------------others---------",other)
                    # if other=="machinary":
                    #     a=machinarymodel.objects.get(id=int(id))
                    #     a.available=False
                    #     a.save()
                    transaction_table.objects.create(razorpay_orderid=razorpay_order_id,razorpay_transactionid=payment_id,seva=seva,amount=originalamount,payment_type="Online",user=user,booking=booking)
                    booking.payment=True
                    booking.save()
                    messages.success(request,"Payment Successfull, Please Check Your Email Id for more info")
                    return redirect("dashboard")
                except Exception as e:
                    print(e)
                    subject="Temple Seva Payment Failed"
                    message1=f"Order id: {razorpay_order_id} \n Payment id: {payment_id} \n Amount: {originalamount}Payment Failed Please Try again."
                    customerEmailThread(subject, message1, [str]).start()
                    messages.error(request,"Payment Failed, Please Check Your Email Id for more info")
                    return redirect("sevas")
            else:
                print("----")
                subject="Temple Seva Payment Failed"
                message1=f"Order id: {razorpay_order_id} \n Payment id: {payment_id} \n Amount: {originalamount}Payment Failed Please Try again."
                customerEmailThread(subject, message1, [str]).start()
                messages.error(request,"Payment Failed, Please Check Your Email Id for more info")
                return redirect("sevas")
        except Exception as e:
            print("---",e)
            subject="Temple Seva Payment Failed"
            message1=f"Order id: {razorpay_order_id} \n Payment id: {payment_id} \n Amount: {originalamount}Payment Failed Please Try again."
            customerEmailThread(subject, message1, [str]).start()
            # if we don't find the required parameters in POST data
            messages.error(request,"Payment Failed, Please Check Your Email Id for more info")

            return redirect("sevas")
    else:
        print("----4")
        subject="Temple Seva Payment Failed"
        message1=f"Order id: {razorpay_order_id} \n Payment id: {payment_id} \n Amount: {originalamount}Payment Failed Please Try again."
        customerEmailThread(subject, message1, [str]).start()
        messages.error(request,"Payment Failed, Please Check Your Email Id for more info")
        return redirect("sevas")
    

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