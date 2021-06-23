from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('addCart/<int:product_id>/', views.add_to_cart, name='cartAdd'),
    path('removeCart/<int:product_id>/', views.removeCart, name='cartRemove'),
    path('removeAll/<int:product_id>/', views.removeAll, name='cartRemoveAll'),
    path('checkout/', views.checkout, name='checkout'),
]

