from django.urls import path

from .views import index, charge, success

app_name = "payment"

urlpatterns = [
    path('', index, name='index'),
    path('charge/', charge, name="charge"),
    path('create-payment-intent', charge, name="create-payment-intent"),
    path('success/<str:args>', success, name="success"),
]