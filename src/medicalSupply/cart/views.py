from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

# method to get the session Id
def _cartId(request):
    cart = request.session.session_key # getting the session_id which is cart_id

    # if no session than create a new session
    if not cart:
        cart = request.session.create()
    return cart

#method to add the item to cart
def add_to_cart(request, product_id):
    current_user = request.user

    if current_user.is_authenticated:
        product = Product.objects.get(id=product_id)# get the product

        #as the cart can have multiple products soo we combime the product and cart to get the cart item
        try:
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity += 1 # quantity increace to 1 wen add to cart
            cart_item.save()
        
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                user=current_user,
                quantity = 1,
            )
            cart_item.save()

        return redirect('cart')
    
    else:
        product = Product.objects.get(id=product_id)# get the product
        try:
            cart = Cart.objects.get(cart_id=_cartId(request))# get the cart using the cart_id present in the session

        #if the cart doesnt exixt than create a new cart with the designated id
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id= _cartId(request)

            )
        cart.save()

        #as the cart can have multiple products soo we combime the product and cart to get the cart item
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1 # quantity increace to 1 wen add to cart
            cart_item.save()
        
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                cart=cart,
                quantity = 1,
            )
            cart_item.save()

        return redirect('cart')



#method to remove the cart item
def removeCart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cartItem = CartItem.objects.get(product=product, user=request.user)
    
    else:
        cart = Cart.objects.get(cart_id=_cartId(request))# get the cart using the cart_id present in the session
        cartItem = CartItem.objects.get(product=product, cart=cart)

    if cartItem.quantity > 1:
        cartItem.quantity -=1
        cartItem.save()
    else:
        cartItem.delete()
    return redirect('cart')




#method to remove the cart item all at once
def removeAll(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cartItem = CartItem.objects.get(product=product, user=request.user)
    
    else:
        cart = Cart.objects.get(cart_id=_cartId(request))# get the cart using the cart_id present in the session
        cartItem = CartItem.objects.get(product=product, cart=cart)
    cartItem.delete()
    return redirect('cart')




#method to create the cart with the cart item added
def cart(request, total=0, quantity=0, cart_item=None):
    try:
        tax = 0
        grand_total = 0
        count = 0

        if request.user.is_authenticated:
             cart_item = CartItem.objects.filter(user=request.user, is_active=True)# get the cart item of the user
        
        else:
            cart = Cart.objects.get(cart_id=_cartId(request)) #get the cart base on the cart_id
            cart_item = CartItem.objects.filter(cart=cart, is_active=True)# get the cart item 
        
        for item in cart_item:
            total += (item.product.price * item.quantity)#get the total
            quantity += item.quantity #get the quantity
        
        tax = (2 * total)/100
        grand_total = total + tax

        count = cart_item.count
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cartItem': cart_item,
        'tax': tax,
        'grandTotal': grand_total,
        'count':count,
    }

    return render(request, 'store/cart.html', context)





@login_required(login_url = 'login')
def checkout(request, total=0, quantity=0, cart_item=None):
    try:
        tax = 0
        grand_total = 0
        count = 0
        
        if request.user.is_authenticated:
             cart_item = CartItem.objects.filter(user=request.user, is_active=True)# get the cart item of the user
        
        else:
            cart = Cart.objects.get(cart_id=_cartId(request)) #get the cart base on the cart_id
            cart_item = CartItem.objects.filter(cart=cart, is_active=True)# get the cart item 
        
        for item in cart_item:
            total += (item.product.price * item.quantity)#get the total
            quantity += item.quantity #get the quantity
        
        tax = (2 * total)/100
        grand_total = total + tax

        count = cart_item.count
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cartItem': cart_item,
        'tax': tax,
        'grandTotal': grand_total,
        'count':count,
    }

    return render(request, 'store/checkout.html', context)