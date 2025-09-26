from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator
from account_module.models import CustomUser


class weblog(models.Model):
    name= models.CharField(max_length=100 , verbose_name='اسم')
    image1 = models.ImageField(upload_to='weblog/',null=True , blank=True , verbose_name='عکس ها' )
    madeby = models.CharField(null=True,blank=True, max_length=50)
    is_active= models.BooleanField(default=True , verbose_name='فعال یا غیرفعال؟')
    is_delete= models.BooleanField(default=False , verbose_name='پاک بشه یا نا؟')
    description = models.TextField(null=True , blank=True , verbose_name="توضیح کامل")
    slug = models.SlugField(default='' , blank=True, db_index=True, verbose_name='url عنوان در ')

    def get_absolute_url(self):
        return reverse("blog_details", args=[self.slug])


    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        if not self.slug:  # اگه خالی بود
            self.slug = slugify(self.name)  # از اسم بسازه
        else:
            self.slug = slugify(self.slug)
        super(weblog,self).save()

    class Meta:
        verbose_name = 'وبلاگ'
        verbose_name_plural = 'وبلاگ ها'   

    def __str__(self):
        return self.name    

# Create your models here.
