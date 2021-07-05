
from django.urls import path

from . import views



urlpatterns = [
    path('place_order/', views.place_order, name='placeOrder'),
    path('payments/', views.payments, name='payments'),
    path('orderComplete/', views.order_complete, name='orderComplete'),

]

