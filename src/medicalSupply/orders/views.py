from django.shortcuts import redirect, render
from cart.models import CartItem
from orders.models import Order, OrderProduct
from store.models import Product

from .forms import OrderForm

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import datetime

def payments(request, order_number):

    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
    order.is_ordered = True
    order.save()

    #move cart items to order product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()


        #reduce the quantity once the product is sold
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    #clear the cart
    CartItem.objects.filter(user=request.user).delete()

    #send order revieved email to customer
    mail_subject = 'Thank you for your order'
    message = render_to_string('order/order_receive_email.html', {
        'user': request.user,
        'order': order,
        })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    
    return redirect('orderComplete')



# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user

    # if cart count is less than or equal to zero than redirect back to shopping page
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for item in cart_items:
        total += (item.product.price * item.quantity)#get the total
        quantity += item.quantity #get the quantity
    
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            #store all the billing info inside order table
            data = Order()
            data.user  = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']

            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #generating order number
            year = int(datetime.date.today().strftime('%Y'))
            day = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            date = datetime.date(year,month,day)
            current_date = date.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            
            context = {
                'order': order,
                'cartItem': cart_items,
                'grand_total': grand_total,
                'tax': tax,
                'total': total,

            }

            return render(request, 'order/payment.html', context)
    
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        sub_total = 0
        
        for i in ordered_products:
            sub_total += i.product_price * i.quantity
        
        context ={
            'order': order,
            'order_products': ordered_products,
            'sub_total': sub_total,

        }

        return render(request, 'order/orderComplete.html', context)
    
    except(Order.DoesNotExist):
        return redirect('home')