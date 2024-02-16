from django.contrib import admin
from .models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('details', 'ship', 'customer', 'time')

class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('customer', 'total_item')

class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'first_name', 'last_name', 'email')

class ShippingInformationAdmin(admin.ModelAdmin):
    readonly_fields = ('customer', 'street', 'local_government_area', 'city', 'state', 'mobile')


admin.site.register(Product)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(ShippingInformation, ShippingInformationAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)