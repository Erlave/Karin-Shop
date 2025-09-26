from django.urls import path 
from . import views


urlpatterns = [
    path('home/' ,views.AdminDashboardView.as_view() , name='admin_home'), 
    
    path('user/list/' ,views.UserListView.as_view() , name='user_list'), 
    path('user/create/' ,views.UserCreateView.as_view() , name='user_create'), 
    path('user/delete/<int:pk>/', views.UserDelete.as_view(), name='admin_users_delete'),
    path('users/edit/<int:pk>/', views.UserEditView.as_view(), name='admin_edit_users'),
    
    path('massages/list/', views.ContactMessageListView.as_view(), name='massages_list'),
    path('massages/edit/<int:pk>/', views.ContactMessageDetailView.as_view(), name='massages_edite'),
    path('massages/delete/<int:pk>/', views.contactDelete.as_view(), name='contact_delete'),
    
    path('blog/list/', views.blogListView.as_view(), name='blog_list'),
    path('blog/delete/<int:pk>/', views.blogDelete.as_view(), name='blog_delete'),
    path('blog/edit/<int:pk>/', views.blogUpdateView.as_view(), name='blog_edite'),
    path('blog/add/', views.blogAdd.as_view(), name='blog_add'),
    
    path('order/list/', views.orderListView.as_view(), name='order_list'),
    path('order/delete/<int:pk>/', views.orderDelete.as_view(), name='order_delete'),
    path('order/edit/<int:pk>/', views.orderUpdateView.as_view(), name='order_edite'),

    path('order/details/list/', views.orderdListView.as_view(), name='orderd_list'),
    path('order/details/delete/<int:pk>/', views.orderdDelete.as_view(), name='orderd_delete'),
    path('order/details/edit/<int:pk>/', views.orderdUpdateView.as_view(), name='orderd_edite'),
    
    path('setting/slider/list/', views.sliderListView.as_view(), name='slider_list'),
    path('setting/slider/edit/<int:pk>/', views.slioderUpdateView.as_view(), name='slider_edite'),
    path('setting/slider/add/', views.sliderAdd.as_view(), name='slider_add'),
    path('setting/slider/delete/<int:pk>/', views.sliderDelete.as_view(), name='slider_delete'),
    
    path('setting/footer/list/', views.footerListView.as_view(), name='footer_list'),
    path('setting/footer/edit/<int:pk>/', views.footerUpdateView.as_view(), name='footer_edite'),
    path('setting/footer/delete/<int:pk>/', views.footerDelete.as_view(), name='footer_delete'),
    path('setting/footer/add/', views.footerAdd.as_view(), name='footer_add'),
    
    path('setting/site/list/', views.siteListView.as_view(), name='site_list'),
    path('setting/site/edit/<int:pk>/', views.siteUpdateView.as_view(), name='site_edite'),
    path('setting/site/add/', views.siteAdd.as_view(), name='site_add'),
    path('setting/site/delete/<int:pk>/', views.siteDelete.as_view(), name='site_delete'),
    
    path('setting/serv/list/', views.servListView.as_view(), name='serv_list'),
    path('setting/serv/edit/<int:pk>/', views.servUpdateView.as_view(), name='serv_edite'),
    path('setting/serv/add/', views.servAdd.as_view(), name='serv_add'),
    path('setting/serv/delete/<int:pk>/', views.servDelete.as_view(), name='serv_delete'),

    path('setting/about/list/', views.aboutListView.as_view(), name='about_list'),
    path('setting/about/edit/<int:pk>/', views.aboutUpdateView.as_view(), name='about_edite'),
    path('setting/about/add/', views.aboutAdd.as_view(), name='about_add'),
    path('setting/about/delete/<int:pk>/', views.aboutDelete.as_view(), name='about_delete'),

    path('setting/questions/list/', views.qListView.as_view(), name='q_list'),
    path('setting/questions/edit/<int:pk>/', views.qUpdateView.as_view(), name='q_edite'),
    path('setting/questions/add/', views.qAdd.as_view(), name='q_add'),
    path('setting/questions/delete/<int:pk>/', views.qDelete.as_view(), name='q_delete'),











]
