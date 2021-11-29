from cart.models import Product, Order, OrderDetail
from rest_framework import serializers
from django.db.models import F


class OrderService:

    @classmethod
    def addProductToOrder(cls, instance, product_ids, products):
        order = instance
        if not Product.objects.filter(pk__in=product_ids):
            raise serializers.ValidationError('Product not found')
        if order:
            order_products_ids = []
            new_products = []
            update_product = []
            new_orderdetails = []
            OrderDetail.objects.filter(order=order).exclude(
                product_id__in=product_ids).delete()
            order_products_ids = [str(detail.product_id) for detail in OrderDetail.objects.filter(
                order=order).all() if detail]
            for product in products:
                if product.get('id') not in order_products_ids:
                    new_products.append(product)
                else:
                    update_product.append(product)
            if new_products:
                for new_product in new_products:
                    new_orderdetails.append(OrderDetail(
                        product_id=new_product.get('id'), order=order, price=new_product.get('price'), quantity=new_product.get('quantity')))
            OrderDetail.objects.bulk_create(new_orderdetails)
            if update_product:
                for product in update_product:
                    OrderDetail.objects.filter(order=order, product_id=product.get('id')).update(
                        **{"price": product.get('price'), "quantity": product.get('quantity')})
            total = sum(
                (item.get_total for item in OrderDetail.objects.filter(order=order) if item))
            order.total = total
            order.save()
