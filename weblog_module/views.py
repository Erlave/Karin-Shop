from django.shortcuts import render
from .models import weblog 
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404




# Create your views here.

class WeblogView(ListView):
    model = weblog
    template_name ='weblg_module/weblog_list.html' 
    context_object_name = 'weblog' 
    paginate_by = 5
    
    def get_queryset(self):
        base= super(WeblogView,self).get_queryset()
        data = base.filter(is_active= True)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weblog_count'] = self.get_queryset().count()

        

        return context


class WeblogDetailsView (TemplateView):
    template_name = 'weblog_module/weblog_details.html'

    def get_context_data(self, **kwargs):
        context = super(WeblogDetailsView,self).get_context_data()
        slug = kwargs['slug']
        weblogg=get_object_or_404(weblog, slug=slug)
        
        context = {
            'web': weblogg,
           
                }

        return context