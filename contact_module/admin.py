from django.contrib import admin
from . import models

 
class Contact_admin(admin.ModelAdmin):
    list_display=['subject','is_read_admin']
    list_filter = ['is_read_admin']
    list_editable=['is_read_admin']

    
admin.site.register(models.contact_model,Contact_admin) 