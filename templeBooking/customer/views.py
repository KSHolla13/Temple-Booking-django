from django.shortcuts import render
from django.views import View

# Create your views here.
class cregister(View):
    template_name='customer/register.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 
    
class clogin(View):
    template_name='customer/login.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)   

class dashboard(View):
    template_name='customer/dashboard.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)        