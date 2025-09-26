from django.db import models

# Create your models here.
class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, verbose_name='آدرس')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل')

    top_category=models.BooleanField(default=False,verbose_name='دسـته بندی هـای محبوب ')
    offer =models.BooleanField( default=False,verbose_name=' پیشنهاد شگفت انگیز')
    newest=models.BooleanField(default=False, verbose_name='جدید ترین محصولات ')
    best_seller=models.BooleanField(default=False, verbose_name='محصولات پرفروش ')


    is_main_setting = models.BooleanField(default=False,verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name
    
class about_us(models.Model):
    about_us_text=models.TextField(verbose_name='متن درباره ما سایت')
    about_us_Ourvision=models.TextField(verbose_name='متن چشم‌انداز ما')
    about_img = models.ImageField(upload_to='about_img/', verbose_name='درباره ما عکس ',null=True)
    is_main_about_us = models.BooleanField(verbose_name='فعال بودن ')

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

    def __str__(self):
        return self.about_us_text

class about_us_services(models.Model):
    services_text=models.CharField(max_length=200, verbose_name='خدمات')
    is_main_about_us_services = models.BooleanField(verbose_name='فعال بودن ')

    class Meta:
        verbose_name = 'خدمات'
        verbose_name_plural = 'خدمات'

    def __str__(self):
        return self.services_text

class footer (models.Model):
    footer_about=models.TextField(verbose_name='متن درباره ما فوتر')
    instaLink=models.URLField( max_length=200 , verbose_name='لینک اینستا')
    whatsappLink=models.URLField( max_length=200 , verbose_name='لینک واتساپ')
    youtubeLink=models.URLField( max_length=200 , verbose_name='لینک یوتوب')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')


    class Meta:
        verbose_name = ' فوتر'
        verbose_name_plural = ' فوتر'



class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی لینک های فوتر'

    def __str__(self):
        return self.title

class FooterLink(models.Model):
    Ftitle = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی', related_name='links')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return self.Ftitle
    

class Slider(models.Model):
    url = models.URLField(max_length=500, verbose_name='لینک')
    image = models.ImageField(upload_to='slider/', verbose_name='عکس اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'



class questions(models.Model):
    ques=models.CharField( max_length=200 , verbose_name='سوال')
    answ=models.CharField( max_length=200 , verbose_name='جواب')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

