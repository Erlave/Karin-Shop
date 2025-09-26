from django.urls import path
from . import views

urlpatterns = [
    path('add-to-order', views.add_to_order, name='add_to_order'),
    path('order_page/', views.OrderDetailView.as_view(), name='order_page'),
    path('clear_order_view/', views.ClearOrderView.as_view(), name='clear_order_view'),
    path('remove_order_itemView/<int:detail_id>/', views.RemoveOrderItemView.as_view(), name='remove_order_itemView'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('dashboard_order/', views.dash_order.as_view(), name='dashboard_order'),
    






    # path('request_payment/', views.request_payment, name='request_payment'),
    # path('verify_payment/', views.verify_payment, name='verify_payment'),
]
