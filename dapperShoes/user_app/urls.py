from django.urls import path, include
from . import views
app_name = 'user_app'
urlpatterns = [
    path('user-login',views.user_login,name='user_login'),
    path('user-signup',views.user_signup,name='user_signup'),
    path('user-logout',views.user_logout,name='user_logout'),
    path('user-send-otp',views.user_send_otp,name='user_send_otp'),  #To send OTP
    path('user-otp-verification',views.user_otp_verification,name='user_otp_verification'),
    path('',views.user_index,name='user_index'),
    

    path('user-login/forgot-password',views.forgot_password,name='forgot_password'),
    path('user-login/forgot-password-verification',views.forgot_password,name='forgot_password_verification'),


    path('user-404',views.user_404,name='user_404'),
    path('user-account',views.user_account,name='user_account'),
    path('user-contact',views.user_contact,name='user_contact'),
    path('user-cart',views.user_cart,name='user_cart'),
    path('user-checkout',views.user_checkout,name='user_checkout'),
    path('user-fullwidth',views.user_fullwidth,name='user_fullwidth'),
    path('user-product-full',views.user_product_full,name='user_product_full'),
    path('user-wishlist',views.user_wishlist,name='user_wishlist'),


    # path('user-otp',views.otp,name='otp'),
    # path('user-login/forgot-password',views.password,name='password'),
    # path('user-login/pass-otp',views.Change_pass_otp,name='Change_pass_otp'),
    # path('user-login/change-password',views.Change_password,name='Change_password'),
    #  path('user-otp_verification',views.otp_verification,name="otp_verification"),

    # path('signup/',views.usersignup,name='usersignup'),
    # path('login/',views.userlogin,name='userlogin'),
    # path('logout/',views.userlogout,name='userlogout'),
    # path('verify-otp/',views.verify_otp,name='verify-otp'),
    # path('forget-password/', ForgetPasswordView.as_view(), name='forget_password_login'),--
    # path('verif-forget-password/', VerifyForgetPasswordView.as_view(), name='verify_password_login'),
    # path('enter-new-password/', EnterNewPasswordView.as_view(), name='new_password_login'),
    
]