from django.db import models
from account_module.models import CustomUser
from product_module.models import Product
# Create your models here.



class Order(models.Model):
    PAYMENT_METHODS = (
        ('online', 'پرداخت اینترنتی'),
        ('cod', 'پرداخت درب منزل'),
        ('credit', 'پرداخت اعتباری'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='نهایی شده/ نشده')
    # payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')
    total_price = models.DecimalField(blank=True, null=True,max_digits=12, decimal_places=0, default=0, verbose_name='قیمت کل سفارش')
    first_name = models.CharField(blank=True, null=True,max_length=100, verbose_name="نام")
    last_name = models.CharField(blank=True, null=True,max_length=100, verbose_name="نام خانوادگی")
    province = models.CharField(blank=True, null=True,max_length=100, verbose_name="استان")
    city = models.CharField(blank=True, null=True,max_length=100, verbose_name="شهر")
    address = models.TextField(blank=True, null=True,verbose_name="آدرس")
    phone = models.CharField(blank=True, null=True,max_length=20, verbose_name="تلفن")
    postal_code = models.CharField(blank=True, null=True,max_length=20, verbose_name="کد پستی")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    payment_method = models.CharField(blank=True, null=True,max_length=20, choices=PAYMENT_METHODS, verbose_name="روش پرداخت")


    def __str__(self):
        return f"سبد {self.id} - {self.user}"

    def calculate_total_price(self):
        return sum([item.get_total_price() for item in self.orderdetails_set.all()])
    
    def update_final_price(self):
        self.total_price = self.calculate_total_price()
    


    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش', related_name='orderdetails_set')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.DecimalField(  max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='قیمت نهایی یک محصول')
    count = models.PositiveIntegerField(verbose_name='تعداد')

    def __str__(self):
        return f"{self.product} - {self.count} عدد"

    def get_total_price(self):
        return self.final_price * self.count


    

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'لیست جزئیات سبد خرید'
