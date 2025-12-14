from django.contrib import admin
from .models import Order, OrderItem
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_email', 'total_price', 'created_at')
    inlines = [OrderItemInline]

    # This helps you see the email directly in the order list
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'