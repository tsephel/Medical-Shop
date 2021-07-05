from django.shortcuts import render
from store.models import Product
from category.models import Category


def home(request):
	products = Product.objects.all().filter(is_available=True)
	category = Category.objects.all()[:3]
	user = request.user

	context = {
		'products': products,
		'category': category,
		'user': user
	}

	return render(request, 'home.html', context)

