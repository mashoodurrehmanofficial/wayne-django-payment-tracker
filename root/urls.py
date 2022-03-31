
from django.urls import path
from .views import *
from .auth_views import *
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [ 
    path('', index, name='index'),  
    path('login/', login_page, name='login_page'),  
    path('register/', register_page, name='register_page'),  
    path('verify_email_account/<str:auth_code>', verifyEmailAccount, name='verify_email_account'),  
    path('send_password_rest_link/', sendPasswordResetLink, name='send_password_rest_link'),  
    path('password_reset_form/<str:password_reset_code>', passwordResetForm, name='password_reset_form'),  
    path('logout/', logout_page, name='logout_page'),  
    path('driver_listing/', index, name='driver_listing'),  
    path('driver_listing/edit_driver/<str:id>', edit_driver, name='edit_driver'),  
    path('driver_listing/delete_driver/<str:id>', delete_driver, name='delete_driver'),  
    path('driver_listing/add_driver/', edit_driver, name='edit_driver'),  
    path('driver_listing/pay_driver/', pay_driver, name='pay_driver'),  
    path('driver_listing/deduct_rent/', deduct_rent, name='deduct_rent'),  
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

