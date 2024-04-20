from django.urls import path, include
from . import views
app_name = 'user_app'
urlpatterns = [
    path('user-login',views.user_login,name='user_login'),
    path('user-signup',views.user_signup,name='user_signup'),
    path('user-logout',views.user_logout,name='user_logout'),
    path('user-send-otp',views.user_send_otp,name='user_send_otp'),  #To send OTP
    path('user-otp-verification',views.user_otp_verification,name='user_otp_verification'),
    
    path('user-login/forgot-password',views.forgot_password,name='forgot_password'),

]