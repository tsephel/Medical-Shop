from django.shortcuts import render
from store.models import Product
from category.models import Category

def home(request):
	products = Product.objects.all().filter(is_available=True)
	category = Category.objects.all()[:3]

	context = {
		'products': products,
		'category': category,
	}

	return render(request, 'home.html', context);