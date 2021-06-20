from django.core import paginator
from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cartId
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None
    
    #showing available products based on the category selected
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        
        #pagination
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)

        count = products.count()#to display number of products
    
    #show all the products available
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

        #pagination
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)

        count = products.count()#to display number of products

    context = {
        'products': page_product,
        'count': count,
    }
    
    return render(request, 'store/store.html', context)

#method to display the single product with category and product slug
def prodcut_detail(request, category_slug, product_slug):
    try:
        detail = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # to check weather the item exists in cart. if true than it doesnt show add button 
        in_cart = CartItem.objects.filter(cart__cart_id=_cartId(request), product=detail).exists()
        

    except Exception as e:
        raise e
    
    context = {
        'detail': detail,
        'in_cart': in_cart,
    }

    return render(request, 'store/product_detail.html', context)


# method to search for products
def search(request):
    if 'search' in request.GET:
        search = request.GET['search']

        if search:
            products = Product.objects.order_by('-created').filter(Q(description__icontains=search) | Q(product_name__icontains=search))
            count = products.count()#to display number of products

    context = {
        'products': products,
        'count': count
    }

    return render(request, 'store/store.html', context)