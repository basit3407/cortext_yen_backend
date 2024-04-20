from django.contrib import admin
from .models import CustomUser, ProductCategory, Fabric, Favorite, Order, OrderItem

admin.site.register(CustomUser)
admin.site.register(ProductCategory)
admin.site.register(Fabric)
admin.site.register(Favorite)
admin.site.register(Order)
admin.site.register(OrderItem)
