from django.urls import path,re_path
from siteflow import views
from siteflow.models import *

     
urlpatterns = [
    
    path("",views.home.as_view(),name="home"),
    path("about-temple",views.aboutTemple.as_view(),name="about-temple"),
    path("calender",views.calender.as_view(),name="calender"),
    path("festivals",views.festivals.as_view(),name="festivals"),
    path("gallery",views.gallery.as_view(),name="gallery"),
    path("sevas",views.sevas.as_view(),name="sevas"),
    path("E-hundi",views.eHundi.as_view(),name="e-hundi"),
    path("seva-details/<slug:slug>",views.sevaDetails.as_view(),name="sevaDetails"),
    # path("seva-details/payment",views.razorpay.as_view(),name="razorpay"),
]