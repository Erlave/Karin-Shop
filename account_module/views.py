import re
import time
import random
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model , login , logout ,get_user_model ,update_session_auth_hash ,authenticate
from requests import session
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from kavenegar import *
from utils.sms_service import send_sms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()

def code_gen(request,username):

    # تولید کد 5 رقمی
    code = str(random.randint(10000, 99999))

    # ذخیره کد و شماره در سشن
    request.session['otp_code'] = code
    request.session['otp_phone'] = username

    request.session['otp_expire'] = time.time() + 180  # انقضا بعد از 3 دقیقه

    request.session.modified = True  # این باعث میشه حتماً ذخیره بشه

    # اینجا در آینده SMS ارسال می‌کنیم - فعلاً تست با print
    print(f"کد ارسال شده به {username} : {code}")
    # send_sms(username , f"کد ورود به کارین شاپ : {code}")

    


class LoginStartView(View):
    template_name = 'account_module/login_register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('Login_input').strip()

        phone_pattern = r'^09\d{9}$'
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if re.match(phone_pattern, username):
           
        
            request.session["username"] = username

            code_gen(request,username)

            return redirect('code_page')

        elif re.match(email_pattern, username):
            # ایمیل → بررسی کاربر
            if User.objects.filter(email=username).exists():

                request.session['login_email'] = username
                return redirect('password_page')
            else:
                messages.error(request,"کاربری با این ایمیل وجود ندارد." )

                return render(request, self.template_name,)
        else:
            # messages.error(request, "ایمیل یا شماره تلفن معتبر وارد کنید.")
            return render(request, self.template_name)


class PasswordLoginView(View):
    template_name = 'account_module/password_page.html'

    def get(self, request):
        if not request.session.get('login_email'):
            messages.error(request, "جلسه منقضی شده؛ دوباره تلاش کنید.")
            return redirect('login_url')
        return render(request, self.template_name)

    def post(self, request):
        email = request.session.get('login_email')
        if not email:
            messages.error(request, "جلسه منقضی شده؛ دوباره تلاش کنید.")
            return redirect('login_url')

        password = request.POST.get('password', '')

        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "کاربری با این ایمیل پیدا نشد.")
            return redirect('login_url')

        # authenticate باید با USERNAME_FIELD صدا زده شود (phone_number)
        user_auth = authenticate(request, username=user.phone_number, password=password)
        if user_auth is None:
            messages.error(request, "رمز عبور اشتباه است.")
            return render(request, self.template_name, status=401)

        login(request, user_auth)
        request.session.pop('login_email', None)
        return redirect('home')






class VerifyCodeView(View):
  
    template_name = 'account_module/confirm_code.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
    
        # --- حالت ارسال مجدد (resend) ---
        if 'resend' in request.POST:
            username = request.session.get('otp_phone')
            
            if not username:
                messages.error(request, "جلسه منقضی شده؛ لطفاً شماره را دوباره وارد کنید.")
                return redirect('login_url')
            # دوباره تولید کد و ذخیره در سشن
            code_gen(request, username)
            messages.success(request, "کد جدید ارسال شد.")
            return redirect('code_page')


        # گرفتن هر ۵ رقم جداگانه و چسبوندن
        digits = [
            request.POST.get('digit1', '').strip(),
            request.POST.get('digit2', '').strip(),
            request.POST.get('digit3', '').strip(),
            request.POST.get('digit4', '').strip(),
            request.POST.get('digit5', '').strip(),

        ]
        entered_code = ''.join(digits)

        session_code = request.session.get('otp_code')
        phone = request.session.get('otp_phone')

        if not phone or not session_code:
            messages.error(request, "جلسه منقضی شده است. دوباره تلاش کنید.")
            return redirect('login_url')

        expire_time = request.session.get('otp_expire')
        if expire_time and time.time() > expire_time:
            messages.error(request, "کد شما منقضی شده است. دوباره تلاش کنید.")
            return redirect('code_page')


        if entered_code == session_code:
            # ویو دوم
            username = request.session.get("username")
             # اگر کاربر وجود نداشت بسازیم
            user, created = User.objects.get_or_create(phone_number=username)
            if created:
                request.session['show_first_login_popup'] = True

            user = User.objects.get(phone_number=phone)
            user.is_active = True
            user.save()
            login(request, user)

            for k in ('otp_code', 'otp_phone', 'otp_expire'):
                if k in request.session:
                    del request.session[k]

            return redirect('home')

            
        else:
            messages.error(request, "کد وارد شده اشتباه است.")
            return redirect('code_page')





@csrf_exempt
def clear_welcome_popup(request):
    if request.method == "POST":
        del request.session['show_first_login_popup']
    return JsonResponse({"success": False})



class ResetPasswordRequestView(View):
    """گرفتن ایمیل از سشن و ارسال کد ریست پسورد"""
    
    def get(self, request):
        # وقتی GET باشه مستقیم چک میکنیم و ریدایرکت میکنیم
        email = request.session.get('login_email')
        if not email:
            messages.error(request, "جلسه منقضی شده است، لطفاً دوباره وارد شوید.")
            return redirect('login_url')

        # بررسی وجود کاربر
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "کاربری با این ایمیل وجود ندارد.")
            return redirect('login_url')

        # ساخت توکن ریست
        token = get_random_string(32)  # رشته تصادفی ۳۲ کاراکتری
        request.session['reset_token'] = token
        request.session['reset_expire'] = time.time() + 600  # ۱۰ دقیقه اعتبار

        # اینجا فعلاً پرینت می‌کنیم (بعداً پیامک)
        print(f"ارسال به شماره {user.phone_number} : لینک ریست → http://127.0.0.1:8007/account/reset-password/confirm/S3cr3tT0k3n={token}/")
        # send_sms(user.phone_number , f" توکن شما برای عوض کردن پسورد :  http://127.0.0.1:8007/account/reset-password/confirm/S3cr3tT0k3n={token}/ ")
        return redirect('reset_password_sent')


class ResetPasswordSentView(View):
    """صفحه‌ای که به کاربر میگه لینک ارسال شد"""

    template_name = 'account_module/reset_sent.html'

    def get(self, request):
        return render(request, self.template_name)



class ResetPasswordConfirmView(View):
    template_name = 'account_module/reset_password.html'

    def get(self, request, token):
        # چک کنیم توکن موجود و معتبر باشه
        session_token = request.session.get('reset_token')
        expire_time = request.session.get('reset_expire')

        if not session_token or token != session_token:
            messages.error(request, "لینک ریست پسورد نامعتبر است.")
            return redirect('login_url')

        if time.time() > expire_time:
            messages.error(request, "لینک ریست پسورد منقضی شده است.")
            return redirect('login_url')

        return render(request, self.template_name)

    def post(self, request, token):
        session_token = request.session.get('reset_token')
        expire_time = request.session.get('reset_expire')
        email = request.session.get('login_email')

        if not email or not session_token or token != session_token:
            messages.error(request, "لینک ریست پسورد نامعتبر است.")
            return redirect('login_url')

        if time.time() > expire_time:
            messages.error(request, "لینک ریست پسورد منقضی شده است.")
            return redirect('login_url')

        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if password1 != password2:
            messages.error(request, "پسوردها یکسان نیستند.")
            return render(request, self.template_name)

        # تغییر پسورد کاربر
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "کاربر یافت نشد.")
            return redirect('login_url')

        user.set_password(password1)
        user.save()

        # پاک کردن سشن‌های مرتبط
        for key in ['reset_token', 'reset_expire', 'login_email']:
            request.session.pop(key, None)

        messages.success(request, "پسورد با موفقیت تغییر کرد. لطفاً وارد شوید.")
        return redirect('login_url')



def logout_view(request):
    logout(request)
    return redirect('home')








