from django.urls import path,re_path
from customer import views
from siteflow.models import *
urlpatterns = [
    path("login",views.user_login.as_view(),name="login"),
    path("registration",views.user_registration.as_view(),name="registration"),
    path("otp",views.registration_otp.as_view(),name="userOtp"),
    path("forgot-password",views.userForgotPassword.as_view(),name="forgotPassword"),
    path("dashboard",views.dashboard.as_view(),name="dashboard"),
    path("logout",views.logout_request,name="logout"),

]