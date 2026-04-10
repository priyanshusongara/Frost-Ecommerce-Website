from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'order_total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'first_name', 'last_name', 'email')
    list_editable = ('status',)  # 🔥 THIS enables quick status change


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)