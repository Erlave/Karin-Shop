from django.contrib import admin
from . import models
# Register your models here.
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['Ftitle', 'url']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['url', 'is_active']
    list_editable = [ 'is_active']

class aboutadmin(admin.ModelAdmin):
    list_display = ['about_us_text', 'is_main_about_us']
    list_editable =[ 'is_main_about_us']

class about_us_services_seadmin(admin.ModelAdmin):
    list_display = ['services_text', 'is_main_about_us_services']
    list_editable =[ 'is_main_about_us_services']


class footeradmin(admin.ModelAdmin):
    list_display = ['footer_about', 'is_active']
    list_editable = [ 'is_active']
class footerboxadmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = [ 'is_active']

class questionsadmin(admin.ModelAdmin):
    list_display = ['ques', 'is_active']
    list_editable = [ 'is_active']

admin.site.register(models.SiteSetting)
admin.site.register(models.footer,footeradmin)
admin.site.register(models.about_us,aboutadmin)
admin.site.register(models.about_us_services,about_us_services_seadmin)
admin.site.register(models.FooterLinkBox,footerboxadmin)
admin.site.register(models.Slider, SliderAdmin)
admin.site.register(models.FooterLink, FooterLinkAdmin)
admin.site.register(models.questions,questionsadmin)
