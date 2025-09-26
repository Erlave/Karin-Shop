from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("شماره موبایل الزامی است.")

        email = self.normalize_email(email) if email else None
        user = self.model(
            phone_number=phone_number,
            email=email,
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # اگه رمز نداره

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(phone_number, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره موبایل")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="ایمیل")
    full_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="نام ونام خانوادگی")
    # last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="نام خانوادگی")
    # avatar=models.ImageField( upload_to='avatars/',default='avatars/default.png', null=True , blank=True)
    # birth_date = models.DateField(blank=True, null=True)
    


    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()
    
    class Meta:

        verbose_name_plural = 'کاربر سفارشی'

    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []  # موقع ساخت ادمین، ایمیل اجباری نیست

    def __str__(self):
        return self.phone_number

