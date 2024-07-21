from django.contrib import admin
from .models import (
    Blog,
    # CustomUser,
    Event,
    ProductCategory,
    Fabric,
    # Favorite,
    # Order,
    # OrderItem,
    # MediaUploads,
    # Order,
    # OrderItem,
)


# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 1


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ("customer_name", "customer_email", "request_number")
#     inlines = [OrderItemInline]

#     def save_model(self, request, obj, form, change):
#         # Save the order first to generate the ID
#         super().save_model(request, obj, form, change)
#         # Ensure the request_number is generated if it does not exist
#         if not obj.request_number:
#             obj.request_number = obj.generate_request_number()
#             obj.save()


# admin.site.register(CustomUser)
admin.site.register(ProductCategory)
admin.site.register(Fabric)
# admin.site.register(Favorite)
# admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(Event)
admin.site.register(Blog)
# admin.site.register(MediaUploads)
