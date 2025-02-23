from django.contrib import admin
from .models import Table, MenuItem, Order, CartItem
from .models import Payment

admin.site.register(Table)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Payment)