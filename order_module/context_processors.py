from .models import Order, OrderDetail
from django.contrib.auth.mixins import LoginRequiredMixin

def cart_products(request ):
    order = None
    cart_items = None
    order_details =None
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, is_paid=False)
            order_details = order.orderdetails_set.all()

            cart_items = order.orderdetails_set.all()
        except Order.DoesNotExist:
            cart_items = None
            order = None
    return {"cart_items": cart_items,
            "order" : order,
            "order_details": order_details,}
    