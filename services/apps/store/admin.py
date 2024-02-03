from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet', 'quantity', 'shipDate', 'status', 'complete']
    search_fields = ['pet__name', 'status']
    list_filter = ['status', 'complete']
    date_hierarchy = 'shipDate'
