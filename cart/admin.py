from django.contrib import admin
from .models import Product, OrderDetail, Order


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
        "price",
        'image',
        'thumbnail',
        "slug",
    )
    search_fields = ("name",)

@admin.register(OrderDetail)
class OrderDetail(admin.ModelAdmin):
    list_display = (
        "product",
        "order",
        "quantity",
    )
    search_fields = ("code",)
    
@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "complete",
        "total",
    )
    search_fields = ("code", "id")   
    order_by = "updated"