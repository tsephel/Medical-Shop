from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('<slug:category_slug>/', views.store, name='productCategory'),
    path('<slug:category_slug>/<slug:product_slug>/', views.prodcut_detail, name='productDetail'),
]

