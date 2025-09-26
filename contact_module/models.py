from django.db import models

# Create your models here.

class contact_model(models.Model):
    subject = models.CharField(max_length=100, verbose_name='عنوان پیام')
    phone_number = models.CharField(max_length=300, verbose_name='شماره تماس')
    message = models.TextField(verbose_name='متن پیام مخاطب')
    admin_message = models.TextField(verbose_name='پیام ادمین')
    is_read_admin = models.BooleanField(default=False, verbose_name='خوانده شده / خوانده نشده')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
    def __str__(self):
        return self.subject
