from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse

import stripe 

stripe.api_key = ('sk_test_51JwLLhHFbz0HMj76pDwHqQFXuokHvgq5ACDQ8SY9WcfcaGhUn3hwhJMYdGB8545KxgyU52G4WD3tVC3NLjX9cd3S00HbGVLm3N')
stripe.ApplePayDomain.create(
  domain_name='drfauthproject.herokuapp.com',
)
# Create your views here.
def index(request):
    return render(request, 'templates/template.html')

def charge(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
    customer = stripe.Customer.create(
        email=request.POST['email'],
        name=request.POST['nickname'],
        source=request.POST['stripeToken']
        )
    charge = stripe.Charge.create(
        customer=customer,
        amount=amount*100,
        currency='usd',
        description="Donation"
        )
    return redirect(reverse('payment:success', args=[amount]))

def success(request, args):
    amount = args
    return render(request, 'templates/success.html', {'amount':amount})