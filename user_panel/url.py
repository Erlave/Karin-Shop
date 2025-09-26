from django.urls import path 
from . import views


urlpatterns = [

    path('account_dashboard/', views.CompleteProfileView.as_view(), name='account_dashboard'),
    path('dashboard_order/', views.dash_order.as_view(), name='dashboard_order'),

]
