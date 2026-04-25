
# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Item, Order
import stripe
from django.views import View



class ItemPageView(View):
    def get(self, request, id):
        item = get_object_or_404(Item, id=id)
        return render(request, 'shop/item.html', {
            'item': item,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY
        })


class BuyItemView(View):    
    def get(self, request, id):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        item = get_object_or_404(Item, id=id)
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {'name': item.name},
                    'unit_amount': item.get_price_in_cents(),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': session.id})


class BuyOrderView(View):    
    def get(self, request, id):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(Order, id=id)
        
        line_items = []
        for order_item in order.orderitem_set.all():
            item = order_item.item
            line_items.append({
                'price_data': {
                    'currency': item.currency,
                    'product_data': {'name': item.name},
                    'unit_amount': item.get_price_in_cents(),
                },
                'quantity': order_item.quantity,
            })
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': session.id})


class PaymentIntentView(View):    
    def get(self, request, id):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        item = get_object_or_404(Item, id=id)
        
        intent = stripe.PaymentIntent.create(
            amount=item.get_price_in_cents(),
            currency=item.currency,
            payment_method_types=['card'],
        )
        return JsonResponse({
            'client_secret': intent.client_secret,
            'id': intent.id
        })


class SuccessView(View):    
    def get(self, request):
        return render(request, 'shop/success.html')


class CancelView(View):    
    def get(self, request):
        return render(request, 'shop/cancel.html')
