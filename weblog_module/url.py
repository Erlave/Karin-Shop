from django.urls import path 
from . import views


urlpatterns = [

    path('blog/', views.WeblogView.as_view(), name='blogg_list'),
    path('blog/<str:slug>', views.WeblogDetailsView.as_view(), name='blog_details'),
    
   

]
