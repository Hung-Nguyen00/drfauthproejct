from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status, permissions
from cart.models import Product, Order, OrderDetail
from cart.api.serializers import ProductSerializer, OrderSerializer, OrderDetailSerializer
from cart.permissions import IsOwnerOrder

# Create your views here.
class CreateProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permissions_class = (permissions.AllowAny,)
    queryset = Product.objects.all()
    
    
class UpdateProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permissions_class = (permissions.AllowAny,)
    queryset = Product.objects.all()    
    

class CreateOrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permissions_class = (permissions.IsAuthenticated, IsOwnerOrder)
    queryset = Order.objects.all()

    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(customer=self.request.user)


class RetrieveUpdateOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permissions_class = (permissions.IsAuthenticated, IsOwnerOrder)
    queryset = Order.objects.all()

    def query_object(self, request):
        return self.queryset.filter(user=request.user, complete=False).last()
    
class CreateOrderDetailView(generics.ListCreateAPIView):
    serializer_class = OrderDetailSerializer
    permissions_class = (permissions.IsAuthenticated)
    queryset = OrderDetail.objects.all()
    
    def get_queryset(self):
        try:
            order = Order.objects.get(customer=self.request.user, complete=False)
        except Order.DoesNotExist:
            raise Response({'error': 'Order not found'})
        return self.queryset.filter(order=order)
    