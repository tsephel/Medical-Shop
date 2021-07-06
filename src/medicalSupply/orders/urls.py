
from django.urls import path

from . import views



urlpatterns = [
    path('place_order/', views.place_order, name='placeOrder'),
    path('payments/<int:order_number>/', views.payments, name='payments'),
    path('orderComplete/', views.order_complete, name='orderComplete'),

]

