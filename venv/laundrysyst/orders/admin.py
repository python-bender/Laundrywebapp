from django.contrib import admin
from .models import ClothType, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'customer', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_code', 'customer__username')
    inlines = [OrderItemInline]

admin.site.register(ClothType)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
