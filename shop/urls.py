from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>/', views.ItemPageView.as_view(), name='item'),
    path('buy/<int:id>/', views.BuyItemView.as_view(), name='buy'),
    path('buy-order/<int:id>/', views.BuyOrderView.as_view(), name='buy-order'),
    path('payment-intent/<int:id>/', views.PaymentIntentView.as_view(), name='payment-intent'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]
