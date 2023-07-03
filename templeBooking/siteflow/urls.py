from django.urls import path,re_path
from siteflow import views
from siteflow.models import *

     
urlpatterns = [
    
    path("",views.home.as_view(),name="home"),

]