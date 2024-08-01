from django.contrib import admin
from .models import (
    Blog,
    BlogCategory,
    ContactDetails,
    CustomUser,
    Event,
    FabricColorImage,
    ProductCategory,
    Fabric,
    Cart,
    Favorite,
    Order,
    OrderItem,
    MediaUploads,
    ContactRequest,
    Subscription,
)


class FabricColorImageInline(admin.TabularInline):
    model = FabricColorImage
    extra = 1  # Number of extra forms to display


class FabricAdmin(admin.ModelAdmin):
    inlines = [FabricColorImageInline]
    list_display = ("title", "product_category", "item_code", "is_hot_selling")
    search_fields = ("title", "product_category__name", "item_code")

    def save_model(self, request, obj, form, change):
        # Call the custom validation method
        obj.clean()
        # Save the object if validation passes
        super().save_model(request, obj, form, change)


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
admin.site.register(Fabric, FabricAdmin)
admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(ContactRequest)
admin.site.register(BlogCategory)
admin.site.register(ContactDetails)
admin.site.register(Subscription)
# admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(Event)
admin.site.register(Blog)
admin.site.register(MediaUploads)


@admin.register(FabricColorImage)
class FabricColorImageAdmin(admin.ModelAdmin):
    list_display = ("fabric", "color")
    search_fields = ("fabric__title", "color")
