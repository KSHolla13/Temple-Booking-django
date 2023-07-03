from django.urls import path,re_path
from customer import views
from siteflow.models import *

     
urlpatterns = [
    
    path("login",views.clogin.as_view(),name="login"),
    path("registration",views.cregister.as_view(),name="registration"),
    path("dashboard",views.dashboard.as_view(),name="dashboard"),

]