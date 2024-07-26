from django.contrib import admin
from .models import (
    Blog,
    CustomUser,
    Event,
    ProductCategory,
    Fabric,
    Cart,
    Favorite,
    Order,
    OrderItem,
    MediaUploads,
    ContactRequest,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("get_customer_name", "get_customer_email", "order_date")
    inlines = [OrderItemInline]

    def get_customer_name(self, obj):
        return obj.user.name

    get_customer_name.short_description = "Customer Name"

    def get_customer_email(self, obj):
        return obj.user.email

    get_customer_email.short_description = "Customer Email"


admin.site.register(CustomUser)
admin.site.register(ProductCategory)
admin.site.register(Fabric)
admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(ContactRequest)
# admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(Event)
admin.site.register(Blog)
admin.site.register(MediaUploads)
