from django.contrib import admin
# Register your models here.

from .models import Item, Discount, Tax, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency', 'created_at']
    list_filter = ['currency']
    search_fields = ['name', 'description']



@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage', 'stripe_coupon_id']



@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage', 'stripe_tax_rate_id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_total', 'paid', 'created_at']
    list_filter = ['paid']
    inlines = [OrderItemInline]

    def get_total(self, obj):
        return f"{obj.get_total_price():.2f} руб"
    get_total.short_description = 'Сумма'


