from django.contrib import admin
from .models import (
    Blog,
    CustomUser,
    Event,
    ProductCategory,
    Fabric,
    Favorite,
    Order,
    OrderItem,
    MediaUploads,
)

admin.site.register(CustomUser)
admin.site.register(ProductCategory)
admin.site.register(Fabric)
admin.site.register(Favorite)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Event)
admin.site.register(Blog)
admin.site.register(MediaUploads)
