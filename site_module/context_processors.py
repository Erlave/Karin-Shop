from .models import SiteSetting
from django.shortcuts import render


def site_settings(request):
    setting = SiteSetting.objects.filter(is_main_setting=True).first()
    return {'site_setting': setting}



def custom_page_not_found(request, exception=None):
    return render(request, 'my_404.html', status=404)