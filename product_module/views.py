from django.shortcuts import render
from .models import Product , Category
from django.views.generic import ListView 
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from product_module.models import Shoes , Clothing ,GameEquipment , GymEquipment , Accessories ,ProtectiveGear ,Supplements
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Product
# Create your views here.


# def product_view (request):
#     return render (request , 'product_module/shop_page.html')


class ProductListView(ListView):
    model = Product
    template_name = 'product_module/shop_page.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        base = super().get_queryset()
        data = base.filter(is_active=True)

        # فیلتر بر اساس دسته‌بندی
        category_id = self.request.GET.get("category")
        if category_id:
            data = data.filter(category_id=category_id)

        # فیلتر بر اساس سرچ
        query = self.request.GET.get("q")
        if query:
            data = data.filter(name__icontains=query)  # سرچ در نام محصول
            # می‌تونی توضیحات یا برند هم اضافه کنی
            # data = data.filter(Q(nameicontains=query) | Q(descriptionicontains=query))
            
            
        in_stock = self.request.GET.get("in_stock")
        if in_stock == "1":
            data = data.filter(stock__gt=0)
        if self.request.GET.get("today_shipping") == "1":
            data = data.filter(today=True)
            
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.get_queryset().count()
        context['selected_category'] = self.request.GET.get("category")
        context['search_query'] = self.request.GET.get("q", "")
        context['category'] = Category.objects.filter(is_active=True)
        return context




def live_search(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )[:5]

    return render(request, "product_module/search_results.html", {"results": results})


class ProductDetailsView(TemplateView):
    template_name = 'product_module/details.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailsView, self).get_context_data(**kwargs)
        slug = kwargs['slug']
        product = get_object_or_404(Product, slug=slug)

        # نوع محصول و دیتای اضافی
        if hasattr(product, 'shoes'):
            extra_data = product.shoes
            product_type = 'shoes'
        elif hasattr(product, 'clothing'):
            extra_data = product.clothing
            product_type = 'clothing'
        elif hasattr(product, 'game_equipment'):
            extra_data = product.game_equipment
            product_type = 'game_equipment'
        elif hasattr(product, 'gym_equipment'):
            extra_data = product.gym_equipment
            product_type = 'gym_equipment'
        elif hasattr(product, 'accessories'):
            extra_data = product.accessories
            product_type = 'accessories'
        elif hasattr(product, 'protective_gear'):
            extra_data = product.protective_gear
            product_type = 'protective_gear'
        elif hasattr(product, 'supplements'):
            extra_data = product.supplements
            product_type = 'supplements'
        else:
            raise Http404()

        # محصولات مرتبط: همون دسته‌بندی + حذف خود محصول
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:6]

        context.update({
            'products': product,
            'extra_data': extra_data,
            'product_type': product_type,
            'related_products': related_products,
        })

        return context
        

# @login_required
# def toggle_favorite_ajax(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     fav_obj, created = Favorite.objects.get_or_create(user=request.user, product=product)

#     if not created:
#         fav_obj.delete()
#         favorited = False
#     else:
#         favorited = True

#     # می‌توانیم تعداد کل علاقه‌مندی‌ها را هم ارسال کنیم (اختیاری)
#     total_favorites = Favorite.objects.filter(product=product).count()
#     return JsonResponse({'favorited': favorited, 'total_favorites': total_favorites})


