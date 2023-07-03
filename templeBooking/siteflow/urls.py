from django.urls import path,re_path
from siteflow import views
from siteflow.models import *

     
urlpatterns = [
    
    path("",views.home.as_view(),name="home"),
    path("sevas",views.sevas.as_view(),name="sevas"),
    path("seva-details",views.sevaDetails.as_view(),name="sevaDetails"),

]