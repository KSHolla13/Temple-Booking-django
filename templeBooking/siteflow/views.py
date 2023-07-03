from django.shortcuts import render
from django.views import View
# Create your views here.


class home(View):
    template_name='siteflow/home.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 
    
class sevas(View):
    template_name='siteflow/sevas.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 

class sevaDetails(View):
    template_name='siteflow/sevaBookView.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)     