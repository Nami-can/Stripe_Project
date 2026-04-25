from django.db import models


class Item(models.Model):

    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('rub', 'RUB'),
    ]

    name = models.CharField("Названия", max_length=100)
    description = models.CharField("Описания", max_length=200)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    currency = models.CharField("Валюта", choices=CURRENCY_CHOICES, max_length=3, default='rub')
    created_at = models.DateTimeField("Дата создания",auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_price_in_cents(self):
        return(int(self.price * 100))
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'



class Discount(models.Model):
    name = models.CharField("Названия скидки", max_length=100)
    percentage = models.IntegerField("Процент скидки",help_text="Процент скидки (0-100)")
    stripe_coupon_id = models.CharField("ID - stripe",max_length=100, blank=True)

    def __str__(self):
        return f'{self.name} - ({self.percentage}%)'
    
    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
    


class Tax(models.Model):
    name = models.CharField("Названия Налога", max_length=100)
    percentage = models.IntegerField("Процент налога",help_text="Процент налога (0-100)")
    stripe_tax_rate_id = models.CharField("ID - налоговой ставки Stripe",max_length=100, blank=True)

    def __str__(self):
        return f'{self.name} - ({self.percentage}%)'
    
    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'




class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem', verbose_name='Товар')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Скидка')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Налог')

    created_at = models.DateTimeField("Дата создания заказа",auto_now_add=True)
    paid = models.BooleanField(default=False, verbose_name='Оплачен?')

    def get_total_price(self):
        total = sum(item.price * order_item.quantity for item, order_item in 
                    zip(self.items.all(), self.orderitem_set.all() ))
        
        return total
    
    def __str__(self):
        return f"Заказ #{self.id}"
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')

    quantity = models.PositiveIntegerField("Количество",default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
    
    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'






