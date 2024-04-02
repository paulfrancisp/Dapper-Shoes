from django.urls import path, include
from . import views
app_name = 'user_app'
urlpatterns = [
    path('user-login',views.user_login,name='user_login'),
    path('user-signup',views.user_signup,name='user_signup'),
    path('user-logout',views.user_logout,name='user_logout'),
    path('user-send-otp',views.user_send_otp,name='user_send_otp'),  #To send OTP
    path('user-otp-verification',views.user_otp_verification,name='user_otp_verification'),
    # path('',views.user_index,name='user_index'),
    

    path('user-login/forgot-password',views.forgot_password,name='forgot_password'),
    # path('user-login/forgot-password-verification',views.forgot_password,name='forgot_password_verification'),


    # path('user-404',views.user_404,name='user_404'),
    # path('user-account',views.user_account,name='user_account'),
    # path('user-contact',views.user_contact,name='user_contact'),
    # path('user-cart',views.user_cart,name='user_cart'),
    # path('user-checkout',views.user_checkout,name='user_checkout'),
    # path('user-wishlist',views.user_wishlist,name='user_wishlist'),
    # path('user-fullwidth',views.user_fullwidth,name='user_fullwidth'),
    # path('user-product-full',views.user_product_full,name='user_product_full'),
    
    
]