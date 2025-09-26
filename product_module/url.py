from django.urls import path 
from . import views


urlpatterns = [
    path('productlist/' ,views.ProductListView.as_view() , name='shop'),
    path('product/<str:slug>', views.ProductDetailsView.as_view() , name='product_details'),
    # path('product/<int:product_id>/favorite-toggle/', views.toggle_favorite_ajax, name='toggle_favorite_ajax'),
    path('live-search/', views.live_search, name='live_search'),
    
]
