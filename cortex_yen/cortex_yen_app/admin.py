from django.contrib import admin
from .models import CustomUser, Event, ProductCategory, Fabric, Favorite, Order, OrderItem

admin.site.register(CustomUser)
admin.site.register(ProductCategory)
admin.site.register(Fabric)
admin.site.register(Favorite)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Event)
