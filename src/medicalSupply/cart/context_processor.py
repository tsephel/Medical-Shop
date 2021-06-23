from .models import Cart, CartItem
from .views import _cartId

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cartId(request))
            
            if request.user.is_authenticated:
                cart_item = CartItem.objects.all().filter(user=request.user)

            else:
                cart_item = CartItem.objects.all().filter(cart=cart[:1])
            for item in cart_item:
                cart_count += item.quantity

        except Cart.DoesNotExist:
            cart_count = 0
    
    return dict(cart_count=cart_count)
