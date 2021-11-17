from django.urls import path
from cart.api.views import CreateProductView, UpdateProductView, CreateOrderView, CreateOrderDetailView

urlpatterns = [
    path('products/', CreateProductView.as_view(), name='product'),
    path('product/<uuid:pk>/', UpdateProductView.as_view(), name='update_product'),
    path('order/', CreateOrderView.as_view(), name='order'),
    path('cart/', CreateOrderDetailView.as_view(), name='cart')
]