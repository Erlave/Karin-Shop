from django.urls import path 
from . import views


urlpatterns = [
    path('login/' ,views.LoginStartView.as_view(), name='login_url'),
    path('confirm_code/' ,views.VerifyCodeView.as_view(), name='code_page'),
    path('confirm_pass/' ,views.PasswordLoginView.as_view(), name='password_page'),
    path('logout/', views.logout_view, name='logout'),
    # path('account_dashboard/', views.CompleteProfileView.as_view(), name='account_dashboard'),
    path('reset-password/request/', views.ResetPasswordRequestView.as_view(), name='reset_password_request'),
    path('reset-password/sent/',views. ResetPasswordSentView.as_view(), name='reset_password_sent'),
    path('reset-password/confirm/S3cr3tT0k3n=<str:token>/', views.ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    path('clear_welcome_popup/', views.clear_welcome_popup, name='clear_welcome_popup'),
    # path('test_cache/', views.test_cache, name=''),
    
    

]
