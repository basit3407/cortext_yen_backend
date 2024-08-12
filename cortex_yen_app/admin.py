from django.contrib import admin
from django.core.exceptions import ValidationError
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
        # Save the object first without validation
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # Save the related objects first
        super().save_related(request, form, formsets, change)
        # Perform the validation after saving related objects
        try:
            form.instance.validate_color_images()
        except ValidationError as e:
            # Delete the main object if validation fails
            form.instance.delete()
            # Raise the validation error to display it in the admin
            raise ValidationError(e)


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


from django.contrib import admin
from .models import ContactRequest


class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_number",
        "user",
        "request_type",
        "current_status_or_order_status",
        "created_at",
    )

    list_filter = ("request_type", "current_status", "order_status")

    def get_form(self, request, obj=None, **kwargs):
        """
        Override get_form to customize the fields based on request_type.
        """
        form = super(ContactRequestAdmin, self).get_form(request, obj, **kwargs)
        if obj:  # When editing an existing object
            if obj.request_type == "product_request":
                # Show order_status, hide current_status
                form.base_fields["order_status"].required = True
                form.base_fields["current_status"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
            else:
                # Show current_status, hide order_status
                form.base_fields["order_status"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
                form.base_fields["current_status"].required = True
        return form

    def current_status_or_order_status(self, obj):
        """
        Display the correct status field based on the request_type.
        """
        if obj.request_type == "product_request":
            return obj.order_status
        return obj.current_status

    current_status_or_order_status.short_description = "Status"

    current_status_or_order_status.short_description = "Status"


admin.site.register(ContactRequest, ContactRequestAdmin)
