from django.shortcuts import render
from product_module.models import Category , Product
from django.views.generic.base import TemplateView
from site_module.models import Slider, SiteSetting, FooterLinkBox, FooterLink ,about_us,about_us_services ,footer,questions 
from requests import session
from django.utils import timezone
from datetime import timedelta

# Create your views here.


# def home_view(request):
#     category = Category.objects.filter(is_active=True)

#     context = {
#         'category' : category
#     }
#     return render (request , 'homes/home_page.html' , context)

    
class homeView(TemplateView):
    template_name = 'homes/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(is_active=True)
        offer =Product.objects.filter(is_active=True ,offer=True )
        
        weekago = timezone.now() - timedelta(days = 7)
        newest = Product.objects.filter(is_active=True , created_at__gte =weekago)
        
        best_seller = Product.objects.filter(is_active=True , best_seller=True)
        
        
        context['seller'] = best_seller
        context['newest'] = newest
        context ['category'] = category
        context ['offer'] = offer
        
        
        return context
        

class AboutView(TemplateView):
    template_name = 'homes/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        about_us_setting: about_us = about_us.objects.filter(is_main_about_us=True).first()
        about_us_services_setting:about_us_services=about_us_services.objects.filter(is_main_about_us_services=True)
        context['about_us_services_setting'] = about_us_services_setting
        context['about_us_setting'] = about_us_setting
        return context



class questions_view(TemplateView):
    template_name = 'homes/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question:questions = questions.objects.filter(is_active=True)
        context['question'] = question
        return context




def header_home_component(request):
    category = Category.objects.filter(is_active=True)
    sliders = Slider.objects.filter(is_active=True)
    context = {
        'category' : category,
        'sliders' :sliders,
    }
    
    return render(request, 'header_home_component.html',context )


def footer_home_component(request):
    Footer =footer.objects.filter(is_active=True).first()
    footerlink=FooterLink.objects.all()
    footerlinkbox=FooterLinkBox.objects.filter(is_active=True)

    context={
        'footer' : Footer,
        'footerlink' :footerlink,
        'footerlinkbox':footerlinkbox,
    }


    return render(request, 'footer_home_component.html', context)




def header_else_component(request):
    category = Category.objects.filter(is_active=True)

    context = {
        'category' : category,

    }
    return render(request, 'header_else_component.html' ,context)


def footer_else_component(request):
    Footer =footer.objects.filter(is_active=True).first()
    footerlink=FooterLink.objects.all()
    footerlinkbox=FooterLinkBox.objects.filter(is_active=True)

    context={
        'footer' : Footer,
        'footerlink' :footerlink,
        'footerlinkbox':footerlinkbox,
    }

    return render(request, 'footer_else_component.html',context )

