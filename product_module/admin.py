from django.contrib import admin
from .models import (
    Category, Product,
    Shoes, Clothing, GameEquipment, GymEquipment,
    Accessories, ProtectiveGear, Supplements ,SubCategory,color,shosesizes,Clothingsizes,Clothingfabric 
)
from django import forms
# Register your models here.


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['__str__','price','is_active' , 'off','is_off']
#     list_filter = ['price','is_active']
#     list_editable = ['price','is_active', 'off','is_off']


# admin.site.register(models.Product , ProductAdmin)
# admin.site.register(models.Category)

class ShoesAdminForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = '__all__'
        widgets = {
            'available_colors': forms.CheckboxSelectMultiple(),
            'available_sizes': forms.CheckboxSelectMultiple(),  # این خط مهمه
        }

class ClothingAdminForm(forms.ModelForm):
    class Meta:
        model = Clothing
        fields = '__all__'
        widgets = {
            'colors': forms.CheckboxSelectMultiple(),
            'sizes': forms.CheckboxSelectMultiple(),
            'fabric_material': forms.CheckboxSelectMultiple(),

              # این خط مهمه
        }

class GymEquipmentAdminForm(forms.ModelForm):
    class Meta:
        model = GymEquipment
        fields = '__all__'
        widgets = {
            'color': forms.CheckboxSelectMultiple(),


              # این خط مهمه
        }

class AccessoriesAdminForm(forms.ModelForm):
    class Meta:
        model = GymEquipment
        fields = '__all__'
        widgets = {
            'color': forms.CheckboxSelectMultiple(),


              # این خط مهمه
        }

class ProtectiveGearAdminForm(forms.ModelForm):
    class Meta:
        model = ProtectiveGear
        fields = '__all__'
        widgets = {
            'color': forms.CheckboxSelectMultiple(),
            'size': forms.CheckboxSelectMultiple(),


              # این خط مهمه
        }




# Inline ها برای نمایش مدل‌های جزئیات داخل صفحه Product
class ShoesInline(admin.StackedInline ):
    model = Shoes
    form = ShoesAdminForm 
    extra = 0


class ClothingInline(admin.StackedInline):
    model = Clothing
    form = ClothingAdminForm
    extra = 0


class GameEquipmentInline(admin.StackedInline):
    model = GameEquipment
    extra = 0


class GymEquipmentInline(admin.StackedInline):
    model = GymEquipment
    form = GymEquipmentAdminForm
    extra = 0


class AccessoriesInline(admin.StackedInline):
    model = Accessories
    form=AccessoriesAdminForm
    extra = 0


class ProtectiveGearInline(admin.StackedInline):
    model = ProtectiveGear
    form = ProtectiveGearAdminForm
    extra = 0


class SupplementsInline(admin.StackedInline):
    model = Supplements
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category",'subcategory', 'off_percent','is_off','stock' ,'today')
    list_editable=['off_percent','is_off', "price",'today']
    list_filter = ("category",)
    search_fields = ("name",)
    # اضافه کردن تمام inlines
    inlines = [
        ShoesInline,
        ClothingInline,
        GameEquipmentInline,
        GymEquipmentInline,
        AccessoriesInline,
        ProtectiveGearInline,
        SupplementsInline,
    ]

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",'is_active')
    list_editable=['is_active']
    search_fields = ("name",)





# اگر بخوای هر مدل جداگانه هم قابل دسترس باشه (اختیاری):
# admin.site.register(Shoes)
# admin.site.register(Clothing)
# admin.site.register(GameEquipment)
# admin.site.register(GymEquipment)
# admin.site.register(Accessories)
# admin.site.register(ProtectiveGear)
# admin.site.register(Supplements)
admin.site.register(color)
admin.site.register(shosesizes)
admin.site.register(Clothingsizes)
admin.site.register(Clothingfabric)







