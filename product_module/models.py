from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator
from account_module.models import CustomUser





class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته')
    is_active= models.BooleanField(default=True , verbose_name='فعال یا غیرفعال؟' ,)
    image = models.ImageField(upload_to='category/',null=True , blank=True , verbose_name='عکس ها' )
    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name



class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories", verbose_name="دسته اصلی")
    name = models.CharField(max_length=100, verbose_name="زیر دسته")
    
    class Meta:
        verbose_name = 'زیر دسته‌'
        verbose_name_plural = 'زیر دسته‌'

    def __str__(self):
        return f"{self.category.name} - {self.name}"




class Product(models.Model):
    name= models.CharField(max_length=100 , verbose_name='اسم')
    image1 = models.ImageField(upload_to='products/',null=True , blank=True , verbose_name='عکس ها' )
    image2 = models.ImageField(upload_to='products/',null=True , blank=True , verbose_name='عکس ها' )
    image3 = models.ImageField(upload_to='products/',null=True , blank=True , verbose_name='عکس ها' )
    image4 = models.ImageField(upload_to='products/',null=True , blank=True , verbose_name='عکس ها' )
    stock = models.PositiveIntegerField(default=0 , verbose_name='موجودی')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products" , null=True, blank=True , verbose_name= 'کتگوری')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products" , null=True, blank=True , verbose_name= ' زیر کتگوری')
    is_active= models.BooleanField(default=True , verbose_name='فعال یا غیرفعال؟')
    is_delete= models.BooleanField(default=False , verbose_name='پاک بشه یا نا؟')
    price = models.IntegerField(default=0, db_index=True ,verbose_name='قیمت')
    short_description = models.CharField(max_length=300, null=True , blank=True , verbose_name='توضیحات کوتاه')
    description = models.TextField(null=True , blank=True , verbose_name="توضیح کامل")
    slug = models.SlugField(default='' , blank=True, db_index=True, verbose_name='url عنوان در ')
    created_at = models.DateTimeField(null=True , blank=True, auto_now_add=True)
    # off = models.IntegerField(default=0 ,null=True,blank=True, db_index=True , verbose_name='تخفیف تومان')
    off_percent = models.IntegerField(default=0,null=True,blank=True, validators=[MinValueValidator(0),MaxValueValidator(100)],db_index=True , verbose_name='تخفیف درصد')
    
    is_off = models.BooleanField(default=False,verbose_name='فعال یا غیرفعال؟تخفیف')
    today = models.BooleanField(default=False,verbose_name='ارسال امروز')
    
    offer =models.BooleanField( default=False,verbose_name=' پیشنهاد شگفت انگیز')

    best_seller=models.BooleanField(default=False, verbose_name='محصولات پرفروش ')

    
    

    def get_price(self):
        if self.is_off:
            off_price=self.price * self.off_percent / 100
            return round(off_price)
        return(self.price)

        
        



    def get_absolute_url(self):
        return reverse("product_details", args=[self.slug])


    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        if not self.slug:  # اگه خالی بود
            self.slug = slugify(self.name)  # از اسم بسازه
        else:
            self.slug = slugify(self.slug)
        super(Product,self).save()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'   

    def __str__(self):
        return self.name    
        

class color(models.Model):
    name= models.CharField( max_length=100)

    def __str__(self):
        return self.name

class shosesizes(models.Model):
    name= models.CharField( max_length=100)

    def __str__(self):
        return self.name


class Clothingsizes(models.Model):
    name= models.CharField( max_length=100)

    def __str__(self):
        return self.name
    
class Clothingfabric(models.Model):
    name= models.CharField( max_length=100)

    def __str__(self):
        return self.name


# 1. کفش ورزشی (Shoes)
class Shoes(models.Model):


    # SIZES = [
    #     ('40', '۴۰'),
    #     ('41', '۴۱'),
    #     ('42', '۴۲'),
    #     ('43', '۴۳'),
    #     ('44', '۴۴'),
    #     ('45', '۴۵'),
    # ]
    # COLORS = [
    #     ('white', 'سفید'),
    #     ('black', 'مشکی'),
    #     ('blue', 'آبی'),
    #     ('red', 'قرمز'),
    #     ('green', 'سبز'),
    # ]

    TYPES = [
        ('running', 'دویدن'),
        ('indoor', 'سالنی'),
        ('football', 'فوتبال'),
        ('basketball', 'بسکتبال'),
        ('all', 'همه‌کاره'),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='shoes', verbose_name="محصول")

    available_sizes = models.ManyToManyField(shosesizes, max_length=20, verbose_name="سایزهای موجود")
    available_colors = models.ManyToManyField(color, verbose_name="رنگ‌های موجود")
    shoe_type = models.CharField(choices=TYPES, max_length=50 , verbose_name="نوع کفش")

    upper_material = models.CharField("جنس رویه", max_length=100)
    sole_material = models.CharField("جنس کفی", max_length=100)
    weight = models.DecimalField("وزن (کیلوگرم)", max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "کفش ورزشی"
        verbose_name_plural = "کفش‌های ورزشی"


# 2. لباس ورزشی (Clothing)
class Clothing(models.Model):

    # SIZE_CHOICES = [
    #     ('S', 'S'),
    #     ('M', 'M'),
    #     ('L', 'L'),
    #     ('XL', 'XL'),
    #     ('XXL', 'XXL'),
    # ]
    # COLOR_CHOICES = [
    #     ('سفید', 'سفید'),
    #     ('مشکی', 'مشکی'),
    #     ('آبی', 'آبی'),
    #     ('قرمز', 'قرمز'),
    #     ('سبز', 'سبز'),
    # ]
    FABRIC_CHOICES = [
        ('پنبه', 'پنبه'),
        ('پلی‌استر', 'پلی‌استر'),
        ('کتان', 'کتان'),
        ('نایلون', 'نایلون'),
    ]
    GENDER_CHOICES = [
        ('مردانه', 'مردانه'),
        ('زنانه', 'زنانه'),
        ('یونیسکس', 'یونیسکس'),
    ]
    CLOTHING_TYPE_CHOICES = [
        ('تی‌شرت', 'تی‌شرت'),
        ('شلوار', 'شلوار'),
        ('سوییشرت', 'سوییشرت'),
        ('ست', 'ست'),
    ]


    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='clothing', verbose_name="محصول")

    sizes = models.ManyToManyField(
        Clothingsizes,
        verbose_name="سایزهای موجود",
        blank=True,
        null=True,
        default=''
    )
    colors = models.ManyToManyField(
        color,
        verbose_name="رنگ‌های موجود",
        blank=True,
        null=True,
        default=''
    )
    fabric_material = models.ManyToManyField(
        Clothingfabric,
        verbose_name="جنس پارچه",
        blank=True,
        null=True,
        default=''
    )
    gender = models.CharField(
        max_length=200,
        choices=GENDER_CHOICES,
        verbose_name="جنسیت",
        blank=True,
        null=True,
        default=''
    )
    clothing_type = models.CharField(
        max_length=200,
        choices=CLOTHING_TYPE_CHOICES,
        verbose_name="نوع لباس",
        blank=True,
        null=True,
        default=''
    )

    class Meta:
        verbose_name = "لباس ورزشی"
        verbose_name_plural = "لباس‌های ورزشی"


# 3. Balls & Game Equipment
class GameEquipment(models.Model):

    
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='game_equipment', verbose_name="محصول")

    equipment_type = models.CharField("نوع وسیله بازی", max_length=50,blank=True, null=True)
    size = models.CharField("سایز", max_length=20,blank=True, null=True)
    weight = models.DecimalField("وزن", max_digits=5, decimal_places=2,blank=True, null=True)
    material = models.CharField("جنس", max_length=50,blank=True, null=True)
    usage = models.CharField("محیط استفاده", max_length=50,blank=True, null=True)

    class Meta:
        verbose_name = "وسایل بازی"
        verbose_name_plural = "توپ و وسایل بازی"


# 4. Gym & Fitness Equipment
class GymEquipment(models.Model):

    # COLOR_CHOICES = [
    #     ('سفید', 'سفید'),
    #     ('مشکی', 'مشکی'),
    #     ('آبی', 'آبی'),
    #     ('قرمز', 'قرمز'),
    #     ('سبز', 'سبز'),
    # ]


    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='gym_equipment', verbose_name="محصول")

    weight = models.DecimalField("وزن", max_digits=6, decimal_places=2)
    dimensions = models.CharField("ابعاد (طول×عرض×ارتفاع)", max_length=100)
    color = models.ManyToManyField(color, max_length=50 ,verbose_name="رنگ",)
    body_material = models.CharField("جنس بدنه", max_length=100)
    equipment_type = models.CharField("نوع وسیله", max_length=50)

    class Meta:
        verbose_name = "لوازم فیتنس"
        verbose_name_plural = "لوازم باشگاهی و فیتنس"


# 5. Accessories
class Accessories(models.Model):

    # COLOR_CHOICES = [
    #     ('سفید', 'سفید'),
    #     ('مشکی', 'مشکی'),
    #     ('آبی', 'آبی'),
    #     ('قرمز', 'قرمز'),
    #     ('سبز', 'سبز'),
    # ]


    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='accessories', verbose_name="محصول")

    accessory_type = models.CharField("نوع لوازم جانبی", max_length=50)
    material = models.CharField("جنس", max_length=50)
    color = models.ManyToManyField(color, max_length=50 ,verbose_name="رنگ",)
    size = models.CharField("سایز / ابعاد", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "لوازم جانبی"
        verbose_name_plural = "لوازم جانبی"


# 6. Protective Gear
class ProtectiveGear(models.Model):

    SIZE_CHOICES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]
    COLOR_CHOICES = [
        ('سفید', 'سفید'),
        ('مشکی', 'مشکی'),
        ('آبی', 'آبی'),
        ('قرمز', 'قرمز'),
        ('سبز', 'سبز'),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='protective_gear', verbose_name="محصول")

    gear_type = models.CharField("نوع تجهیزات ایمنی", max_length=50)
    size = models.ManyToManyField(Clothingsizes, max_length=20 ,verbose_name="سایز")
    material = models.CharField("جنس", max_length=50)
    color = models.ManyToManyField(color, max_length=50 ,verbose_name="رنگ",)

    class Meta:
        verbose_name = "تجهیزات ایمنی"
        verbose_name_plural = "تجهیزات محافظتی و ایمنی"


# 7. Supplements
class Supplements(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='supplements', verbose_name="محصول")

    weight_volume = models.CharField("(کیلو گرم)وزن / حجم بسته", max_length=50)
    flavor = models.CharField("طعم", max_length=50)
    expiration_date = models.DateField("تاریخ انقضا")
    ingredients = models.TextField("ترکیبات اصلی")
    brand = models.CharField("برند", max_length=100)

    class Meta:
        verbose_name = "مکمل"
        verbose_name_plural = "مکمل‌ها"
        
        
# class Favorite(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'product')