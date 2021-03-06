from django.contrib import admin
from .models import Order, OrderProduct

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'status', 'is_ordered']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone']
    list_per_page = 20
    inlines = [OrderProductInline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'user', 'quantity', 'ordered']
    list_filter = ['ordered']
    search_fields = ['product', 'user', 'ordered']
    list_per_page = 20

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)