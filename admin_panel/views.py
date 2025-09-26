from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from product_module.models import Product
from order_module.models import Order
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from contact_module.models import contact_model
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from account_module.models import CustomUser
from weblog_module.models import weblog
from order_module.models import Order ,OrderDetail
from utils.permision import AdminOnlyMixin
from site_module.models import Slider,footer,SiteSetting,about_us_services,about_us,questions



User = get_user_model()

#----------------------------------------------------------
#                          //dashbourd//
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name ="home/dashboard.html"
    login_url = 'login_url'  # اسم URL لاگینت رو اینجا بزار

    # فقط ادمین اجازه دسترسی داشته باشه
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_count'] = Product.objects.count()
        context['orders_count'] = Order.objects.count()
        context['users_count'] = User.objects.count()
        return context


#-----------------------------------------------------------
#                          //user//



class UserListView(LoginRequiredMixin , AdminOnlyMixin,View,):
    login_url = 'login_url'
    def get(self, request):
        users = User.objects.all()
        return render(request, "user/user_list.html", {"users": users})
    
    
    
    

class UserCreateView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        # فقط فرم خالی برگردون
        return render(request, "user/user_add.html")

    def post(self, request):
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        password1 = request.POST.get("password")

        if not email or not password1 :
            messages.error(request, "ایمیل و رمز عبور الزامی است.")
            return redirect("user_create")

        if User.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلاً استفاده شده است.")
            return redirect("user_create")

        if not phone_number:
            messages.error(request, "شماره موبایل الزامی است.")
            return redirect("user_create")

        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "این شماره قبلاً ثبت شده است.")
            return redirect("user_create")

        user = User(email=email, phone_number=phone_number , password=password1)
        # user.set_password(password)
        user.save()

        messages.success(request, "کاربر جدید با موفقیت ایجاد شد.")
        return redirect("user_list")



class UserDelete( AdminOnlyMixin ,LoginRequiredMixin ,DeleteView):
    login_url = 'login_url'
    model = User
    template_name = 'admin_panel/user/user_delete.html'
    success_url = reverse_lazy('user_list')




class UserEditView(LoginRequiredMixin, AdminOnlyMixin ,View):
    login_url = 'login_url'
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, "user/user_edit.html", {"user": user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        password2 = request.POST.get("password", "").strip()

        is_active = request.POST.get("is_active") == "on"
        is_superuser = request.POST.get("is_superuser") == "on"
        is_staff = request.POST.get("is_staff") == "on"

        updated = False

        # full_name
        if full_name != user.full_name:
            if full_name:  # فقط اگه خالی نباشه تغییر بده
                user.full_name = full_name
                updated = True

        # email
        if email != user.email:
            if email:
                if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                    messages.error(request, "این ایمیل قبلاً استفاده شده است.")
                    return redirect("admin_edit_users", pk=pk)
                user.email = email
                updated = True

        # phone_number
        if phone_number != user.phone_number:
            if phone_number:
                if User.objects.filter(phone_number=phone_number).exclude(pk=user.pk).exists():
                    messages.error(request, "این شماره موبایل قبلاً ثبت شده است.")
                    return redirect("admin_edit_users ", pk=pk)
                user.phone_number = phone_number
                updated = True

        # password
        if password2:
            user.set_password(password2)
            updated = True

        # بولین‌ها
        if user.is_active != is_active:
            user.is_active = is_active
            updated = True

        if user.is_superuser != is_superuser:
            user.is_superuser = is_superuser
            updated = True

        if user.is_staff != is_staff:
            user.is_staff = is_staff
            updated = True

        if updated:
            user.save()
            messages.success(request, "اطلاعات کاربر با موفقیت ویرایش شد.")
        else:
            messages.info(request, "هیچ تغییری اعمال نشد.")

        return redirect("user_list")

#------------------------------------------------------------------------------------
#                         //contact//


class ContactMessageListView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        messages_list = contact_model.objects.all().order_by("-id")
        return render(request, "contact_us/contact_list.html", {
            "messages": messages_list
        })


class ContactMessageDetailView(AdminOnlyMixin,LoginRequiredMixin, View):
    def get(self, request, pk):
        contact = get_object_or_404(contact_model, pk=pk)
        return render(request, "contact_us/contact_edite.html", {"contact": contact})

    def post(self, request, pk):
        contact = get_object_or_404(contact_model, pk=pk)

        subject = request.POST.get("subject", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        message = request.POST.get("message", "").strip()
        admin_message = request.POST.get("admin_message", "").strip()

        is_read_admin = request.POST.get("is_read_admin") == "on"


        updated = False

        # subject
        if subject != contact.subject:
            if subject:  # فقط اگه خالی نباشه تغییر بده
                contact.subject = subject
                updated = True

        # phone_number
        if phone_number != contact.phone_number:
            if phone_number:  # فقط اگه خالی نباشه تغییر بده
                contact.phone_number = phone_number
                updated = True

        # message
        if message != contact.message:
            if message:  # فقط اگه خالی نباشه تغییر بده
                contact.message = message
                updated = True

        # admin_message
        if admin_message != contact.admin_message:
            if admin_message:  # فقط اگه خالی نباشه تغییر بده
                contact.admin_message = admin_message
                updated = True

        # بولین‌ها
        if contact.is_read_admin != is_read_admin:
            contact.is_read_admin = is_read_admin
            updated = True



        if updated:
            contact.save()
            messages.success(request, "اطلاعات کاربر با موفقیت ویرایش شد.")
        else:
            messages.info(request, "هیچ تغییری اعمال نشد.")

        return redirect("massages_list")




class contactDelete(LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = contact_model
    template_name = 'contact_us/contact_delete.html'
    success_url = reverse_lazy('massages_list')

#----------------------------------------------------
#             //blog//

class blogListView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        blogs = weblog.objects.all()
        return render(request, "blog/blog_list.html", {"blogs": blogs})
    

class blogDelete(LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = weblog
    template_name = 'blog/blog_list.html'
    success_url = reverse_lazy('blog_list')

    
    
class blogUpdateView(LoginRequiredMixin, AdminOnlyMixin,UpdateView):
    login_url = 'login_url'
    model = weblog
    fields = ['name', 'madeby', 'description', 'is_active', 'image1']
    context_object_name = "blogs"
    template_name = 'blog/edit_blog.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        return super().form_valid(form)
    
    
    
    
class blogAdd(LoginRequiredMixin, AdminOnlyMixin,CreateView):
    login_url = 'login_url'
    model = weblog
    fields = ['name', 'madeby', 'description', 'is_active', 'image1']
    context_object_name = "blogs"
    template_name = 'blog/addd_blog.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)


#---------------------------------------------------------------------------
#                                  //order//

class orderListView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        order = Order.objects.all()
        return render(request, "order/order_list.html", {"order": order})
    
    



class orderDelete(LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = Order
    template_name = 'order/order_list.html'
    success_url = reverse_lazy('order_list')
    
    
    
    
    
        
class orderUpdateView(LoginRequiredMixin, AdminOnlyMixin,UpdateView):
    login_url = 'login_url'
    model = Order
    fields = ['user', 'is_paid', 'total_price', 'first_name', 'last_name', 'province', 'city', 'address', 'phone', 'postal_code', 'description', 'payment_method']
    context_object_name = "order"
    template_name = 'order/edit_order.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        return super().form_valid(form)
    
    
    
    
    
    
class orderdListView(LoginRequiredMixin, AdminOnlyMixin, View):
    login_url = 'login_url'
    def get(self, request):
        OrderD = OrderDetail.objects.all()
        return render(request, "order/orderdetails_list.html", {"OrderD": OrderD})
       
    
    


class orderdDelete( LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = OrderDetail
    template_name = 'order/orderdetails_list.html'
    success_url = reverse_lazy('orderd_list')
    
    
     
class orderdUpdateView( LoginRequiredMixin, AdminOnlyMixin,UpdateView):
    login_url = 'login_url'
    model = OrderDetail
    fields = ['order', 'product', 'final_price', 'count']
    context_object_name = "orderd"
    template_name = 'order/edit_orderd.html'
    success_url = reverse_lazy('orderd_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        return super().form_valid(form)
    
    
    
#-----------------------------------------------------------------------------
#                                //site_setting//

#  *slider*



class sliderListView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        slider = Slider.objects.all()
        return render(request, "site_setting/slider_list.html", {"slider": slider})
    
    



     
class slioderUpdateView( LoginRequiredMixin, AdminOnlyMixin,UpdateView):
    login_url = 'login_url'
    model = Slider
    fields = ['url', 'image', 'is_active']
    context_object_name = "slider"
    template_name = "site_setting/edit_slider.html"
    success_url = reverse_lazy('slider_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        return super().form_valid(form)
    



class sliderAdd(LoginRequiredMixin, AdminOnlyMixin,CreateView):
    login_url = 'login_url'
    model = Slider
    fields = ['url', 'image', 'is_active']
    context_object_name = "slider"
    template_name = "site_setting/add_slider.html"
    success_url = reverse_lazy('slider_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)




class sliderDelete( LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = Slider
    template_name = 'site_setting/edit_slider.html'
    success_url = reverse_lazy('slider_list')
    

#  *footer*



class footerListView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        Footer = footer.objects.all()
        return render(request, "site_setting/footer_list.html", {"footer": Footer})

    


class footerUpdateView( LoginRequiredMixin, AdminOnlyMixin,UpdateView):
    login_url = 'login_url'
    model = footer
    fields = ['footer_about', 'instaLink', 'whatsappLink','youtubeLink','is_active']
    context_object_name = "footer"
    template_name = "site_setting/edit_footer.html"
    success_url = reverse_lazy('footer_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        return super().form_valid(form)
    


class footerDelete( LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = footer
    template_name = 'site_setting/footer_list.html'
    success_url = reverse_lazy('footer_list')





class footerAdd(LoginRequiredMixin, AdminOnlyMixin,CreateView):
    login_url = 'login_url'
    model = footer
    fields = ['footer_about', 'instaLink', 'whatsappLink','youtubeLink','is_active']
    context_object_name = "footer"
    template_name = "site_setting/add_footer.html"
    success_url = reverse_lazy('footer_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)


#  *setting*


class siteListView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        Site = SiteSetting.objects.all()
        return render(request, "site_setting/site_list .html", {"Site": Site})



class siteUpdateView( LoginRequiredMixin, AdminOnlyMixin,UpdateView):
    login_url = 'login_url'
    model = SiteSetting
    fields = ['site_name', 'site_url', 'address','phone','email',    'top_category','offer','newest','best_seller','is_main_setting']
    context_object_name = "site"
    template_name = "site_setting/edit_site.html"
    success_url = reverse_lazy('site_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        return super().form_valid(form)
    


class siteAdd(LoginRequiredMixin, AdminOnlyMixin,CreateView):
    login_url = 'login_url'
    model = SiteSetting
    fields = ['site_name', 'site_url', 'address','phone','email',    'top_category','offer','newest','best_seller','is_main_setting']
    context_object_name = "site"
    template_name = "site_setting/add_site.html"
    success_url = reverse_lazy('site_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)




class siteDelete( LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = SiteSetting
    template_name = 'site_setting/add_site.html'
    success_url = reverse_lazy('site_list')



#  *serv*




class servListView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        serv = about_us_services.objects.all()
        return render(request, "site_setting/serv_list .html", {"serv": serv})


class servUpdateView( LoginRequiredMixin, AdminOnlyMixin,UpdateView):
    login_url = 'login_url'
    model = about_us_services
    fields = ['services_text', 'is_main_about_us_services']
    context_object_name = "serv"
    template_name = "site_setting/edit_serv.html"
    success_url = reverse_lazy('serv_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        return super().form_valid(form)



class servAdd(LoginRequiredMixin, AdminOnlyMixin,CreateView):
    login_url = 'login_url'
    model = about_us_services
    fields = ['services_text', 'is_main_about_us_services']
    context_object_name = "serv"
    template_name = "site_setting/add_serv.html"
    success_url = reverse_lazy('serv_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)
    
    
    
    
    

class servDelete( LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = about_us_services
    template_name = 'site_setting/edit_serv.html'
    success_url = reverse_lazy('serv_list')

    
#  *serv*
    

class aboutListView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        about = about_us.objects.all()
        return render(request, "site_setting/about_list .html", {"about": about})
    
    

class aboutUpdateView( LoginRequiredMixin, AdminOnlyMixin,UpdateView):
    login_url = 'login_url'
    model = about_us
    fields = ['about_us_text', 'about_us_Ourvision','about_img', 'is_main_about_us']
    context_object_name = "about"
    template_name = "site_setting/edite_about.html"
    success_url = reverse_lazy('about_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        return super().form_valid(form)

    
    


class aboutAdd(LoginRequiredMixin, AdminOnlyMixin,CreateView):
    login_url = 'login_url'
    model = about_us
    fields = ['about_us_text', 'about_us_Ourvision','about_img', 'is_main_about_us']
    context_object_name = "about"
    template_name = "site_setting/add_about.html"
    success_url = reverse_lazy('about_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)
    
    

class aboutDelete( LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = about_us
    template_name = 'site_setting/about_list.html'
    success_url = reverse_lazy('about_list')

#  *serv*


class qListView(LoginRequiredMixin, AdminOnlyMixin,View):
    login_url = 'login_url'
    def get(self, request):
        q = questions.objects.all()
        return render(request, "site_setting/q_list.html", {"q": q})
    


class qUpdateView( LoginRequiredMixin, AdminOnlyMixin,UpdateView):
    login_url = 'login_url'
    model = questions
    fields = ['ques', 'answ', 'is_active']
    context_object_name = "q"
    template_name = "site_setting/edit_q.html"
    success_url = reverse_lazy('q_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        return super().form_valid(form)


class qAdd(LoginRequiredMixin, AdminOnlyMixin,CreateView):
    login_url = 'login_url'
    model = questions
    fields =  ['ques', 'answ', 'is_active']
    context_object_name = "q"
    template_name = "site_setting/add_q.html"
    success_url = reverse_lazy('q_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)
    
    
    
    


class qDelete( LoginRequiredMixin, AdminOnlyMixin,DeleteView):
    login_url = 'login_url'
    model = questions
    template_name = 'site_setting/q_list.html'
    success_url = reverse_lazy('q_list')

    
    
    
    
    
    
    