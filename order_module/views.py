from django.shortcuts import render, redirect
from product_module.models import Product
from .models import Order, OrderDetail
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
import requests
import json
import time
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from .models import Product, Order, OrderDetail
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Order, OrderDetail
from product_module.models import Product 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView , View
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required






def add_to_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'not_logged_in',
            'title': 'خطا',
            'text': 'برای افزودن محصول باید وارد حساب کاربری شوید.',
            'icon': 'warning',
            'confirm_button_text': 'ورود به سایت'
        })

    product_id = request.GET.get('product_id')
    count = request.GET.get('count')

    if not product_id or not count :
        return JsonResponse({
            'status': 'error',
            'title': 'خطا',
            'text': 'اطلاعات محصول یا تعداد ارسال نشده است.',
            'icon': 'error',
            'confirm_button_text': 'باشه'
        })
    

    product = get_object_or_404(Product, id=product_id)
    count = int(count)

    

    if count >= product.stock :
        return JsonResponse({
            'status': 'error',
            'title': 'خطا',
            'text':f'موجودی کافی نیست ! فقط {product.stock} موجود است.' ,
            'icon': 'error',
            'confirm_button_text': 'باشه'
        })
    
    if count < 1 :
        return JsonResponse({
            'status': 'error',
            'title': 'خطا',
            'text':'مقدار وارد شده معتبر نیست' ,
            'icon': 'error',
            'confirm_button_text': 'باشه'
        })

    # پیدا کردن یا ساختن سفارش فعال
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)

    # بررسی اینکه محصول قبلاً داخل سفارش هست یا نه
    order_detail, created_detail = OrderDetail.objects.get_or_create(
        order=order,
        product=product,
        defaults={'count': count, 'final_price': product.get_price()}
    )
 # یعنی قبلاً بوده → تعدادشو زیاد کن
    if not created_detail:
        new_count = order_detail.count + count
        if  new_count <= product.stock :
            order_detail.count += count
            order_detail.save()
        else:
            return JsonResponse({
            'status': 'error',
            'title': 'خطا',
            'text':f'موجودی کافی نیست !h فقط {product.stock} موجود است.' ,
            'icon': 'error',
            'confirm_button_text': 'باشه'
        })




    return JsonResponse({
        'status': 'success',
        'title': 'موفق',
        'text': f'{product.name} به سبد خرید اضافه شد.',
        'icon': 'success',
        'confirm_button_text': 'باشه'
    })

class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = "order_module/order.html"
    login_url = 'login_url'

    def get(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(
            user=request.user,
            is_paid=False
        )

        order_details = order.orderdetails_set.all()

        # اگه سبد خالی بود یه صفحه دیگه رندر کن
        if not order_details.exists():
            return render(request, "order_module/empty_cart.html", {})

        context = {
            "order": order,
            "order_details": order_details,
            "total_price": order.calculate_total_price()
        }
        return render(request, self.template_name, context)

class ClearOrderView(View):
    def get(self, request):
        order = Order.objects.filter(user=request.user, is_paid=False).first()
        if order:
            order.orderdetails_set.all().delete()
            # messages.success(request, "سبد خرید شما خالی شد.")
        return render(request ,  "order_module/empty_cart.html")
    
class RemoveOrderItemView(View):
    def get(self, request, detail_id):
        order_detail = OrderDetail.objects.filter(id=detail_id, order__user=request.user, order__is_paid=False).first()
        if order_detail:
            order_detail.delete()
            # messages.success(request, "محصول از سبد خرید حذف شد.")
        return redirect("order_page")
    

class CheckoutView(View , LoginRequiredMixin):
    login_url = 'login_url'
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login_url')
        try:
            order = Order.objects.get(user=request.user, is_paid=False)
            if not order.orderdetails_set.exists():
                return render(request, "order_module/empty_cart.html", {})
        except Order.DoesNotExist:
            return render(request, "order_module/empty_cart.html", {})

        return render(request, 'order_module/checkout.html')

    def post(self, request):
        name = request.POST.get("name")
        family = request.POST.get("family")
        province = request.POST.get("province")
        city = request.POST.get("city")
        address = request.POST.get("address")
        number = request.POST.get("number")
        code_post = request.POST.get("code_post")
        des = request.POST.get("des")
        payment_method = request.POST.get("payment_method")

        if not all([name ,family ,province, city ,address,number,code_post,des,payment_method]):
            return render(request,'order_module/checkout.html',{"error":"لطفا همه فیلد ها رو پر کنید"})

        try:
            order = Order.objects.get(user=request.user, is_paid=False)
            if not order.orderdetails_set.exists():
                return render(request, "order_module/empty_cart.html", {})
        except Order.DoesNotExist:
            return render(request, "order_module/empty_cart.html", {})

        # حالت پرداخت درب منزل
        if payment_method == "credit":
            order.first_name = name
            order.last_name = family
            order.address = address
            order.postal_code = code_post
            order.province = province
            order.city = city
            order.phone = number
            order.description = des
            order.payment_method = "credit"
            order.is_paid = True
            order.update_final_price()
            order.save()
            for detail in order.orderdetails_set.all():
                product = detail.product
                if product.stock >= detail.count:  # چک کنیم منفی نشه
                    product.stock -= detail.count
                    product.save()
                else:
                    raise ValueError(f"موجودی {product.name} کافی نیست.")
            return render(request, "order_module/successful_credit.html", {"order": order})

        # حالت پرداخت آنلاین
        elif payment_method == "online":
            order.first_name = name
            order.last_name = family
            order.address = address
            order.postal_code = code_post
            order.province = province
            order.city = city
            order.phone = number
            order.description = des
            order.payment_method = "online"
            order.is_paid = True
            order.update_final_price()
            order.save()
            
            for detail in order.orderdetails_set.all():
                product = detail.product
                if product.stock >= detail.count:  # چک کنیم منفی نشه
                    product.stock -= detail.count
                    product.save()
                else:
                    raise ValueError(f"موجودی {product.name} کافی نیست.")
                
            return render(request, "order_module/successful_online.html", {"order": order})

        # حالت خطا
        else:
            return render(request, "order_module/failed.html", {"order": order})
        
        
        
        
        
class dash_order(LoginRequiredMixin, TemplateView):
    template_name = "order_module/buys.html"
    login_url = 'login_url'

    def get(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(
            user=request.user,
            is_paid=False
        )

        order_details = order.orderdetails_set.all()

        # اگه سبد خالی بود یه صفحه دیگه رندر کن
        if not order_details.exists():
            return render(request, "order_module/empty_cart.html", {})

        context = {
            "order": order,
            "order_details": order_details,
            "total_price": order.calculate_total_price()
        }
        return render(request, self.template_name, context)