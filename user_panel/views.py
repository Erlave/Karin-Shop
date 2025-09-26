from django.shortcuts import render

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model , login , logout ,get_user_model ,update_session_auth_hash ,authenticate
from requests import session
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from django.shortcuts import render
# from .models import Product , Category
 
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
# from product_module.models import Shoes , Clothing ,GameEquipment , GymEquipment , Accessories ,ProtectiveGear ,Supplements 

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from order_module.models import  Order, OrderDetail 
 
 
 
# Create your views here.
# User = get_user_model()
# class CompleteProfileView(LoginRequiredMixin, View):
#     login_url = 'login_url'

#     def get(self, request):
#         return render(request, 'user_panel/account_dash.html', {
#             'phone_number': request.user.phone_number
#         })

#     def post(self, request):
#         full_name = request.POST.get('full_name')
#         # birth_date = request.POST.get('birth_date')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         old_password = request.POST.get('old_password')
#         new_password = request.POST.get('new_password')
#         new_again_password = request.POST.get('new_again_password')
        





#         # شرط وابستگی ایمیل و پسورد
#         if email and not password:
#             messages.error(request, "وقتی ایمیل وارد می‌کنید، باید رمز عبور هم بگذارید.")
#             return redirect('account_dashboard')

#         if password and not email:
#             messages.error(request, "وقتی رمز عبور وارد می‌کنید، باید ایمیل هم بگذارید.")
#             return redirect('account_dashboard')
        
#         if email:
#             if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
#                 messages.error(request, "این ایمیل قبلاً ثبت شده است.")
#                 return redirect('account_dashboard')
            
#         user = request.user
    

#         # ذخیره تغییرات
        
#         if full_name:
#             user.full_name = full_name
#         if email:
#             user.email = email
#         if password:
#             user.set_password(password)

#         # user.set_password(request.POST['password'])
#         user.save()
#         update_session_auth_hash(request , user)

       
#         return redirect('home')

User = get_user_model()

class CompleteProfileView(LoginRequiredMixin, View):
    login_url = 'login_url'

    def get(self, request):
        return render(request, 'user_panel/account_dash.html', {
            'phone_number': request.user.phone_number
        })

    def post(self, request):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        # حالت ۱ → کاربر هنوز پسورد نداره
        password = request.POST.get('password')  # فقط برای اولین بار

        # حالت ۲ → کاربر پسورد داره
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_again_password = request.POST.get('new_again_password')

        user = request.user

        # ---------------- پروفایل ----------------
        if full_name:
            user.full_name = full_name
        if email:
            # فقط وقتی چک بشه که ایمیل فرستاده شده
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, "این ایمیل قبلاً ثبت شده است.")
                return redirect('account_dashboard')
            user.email = email


        # شرط وابستگی ایمیل و پسورد
        if email and not password:
            messages.error(request, "وقتی ایمیل وارد می‌کنید، باید رمز عبور هم بگذارید.")
            return redirect('account_dashboard')

        if password and not email:
            messages.error(request, "وقتی رمز عبور وارد می‌کنید، باید ایمیل هم بگذارید.")
            return redirect('account_dashboard')
        
        if password:
            user.set_password(password)    
        # ---------------- پسورد ----------------
        if not user.has_usable_password():
            # کاربر برای اولین بار پسورد ست می‌کنه
            if password:
                if not email:
                    messages.error(request, "وقتی رمز عبور وارد می‌کنید باید ایمیل هم بگذارید.")
                    return redirect('account_dashboard')
                user.set_password(password)
            elif email:
                messages.error(request, "وقتی ایمیل وارد می‌کنید باید رمز عبور هم بگذارید.")
                return redirect('account_dashboard')
        else:
            # کاربر پسورد داره → old/new/new_again باید پر بشن
            if old_password or new_password or new_again_password:
                if not user.check_password(old_password):
                    messages.error(request, "پسورد فعلی درست نیست ❌")
                    return redirect('account_dashboard')
                if new_password and new_password == new_again_password:
                    user.set_password(new_password)
                else:
                    messages.error(request, "پسوردهای جدید مطابقت ندارند ❌")
                    return redirect('account_dashboard')

        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "پروفایل شما با موفقیت به‌روز شد ✅")
        return redirect('account_dashboard')
    
class dash_order(LoginRequiredMixin, TemplateView):
    template_name = "user_panel/dashboard_cart.html"
    login_url = 'login_url'

    def get(self, request, *args, **kwargs):
        
        
        
        order = Order.objects.filter(
            user=request.user,
            is_paid=True
        )
        

        

        

        context = {
            
            # "total_price": order.calculate_total_price(),
            "order": order
        }
        return render(request, self.template_name, context)