from django.contrib import admin
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings
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
    readonly_fields = ("order_date",)

    inlines = [OrderItemInline]

    def get_customer_name(self, obj):
        return obj.user.name

    get_customer_name.short_description = "Customer Name"

    def get_customer_email(self, obj):
        return obj.user.email if obj.user else "No email"

    get_customer_email.short_description = "Customer Email"


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


class CustomUserAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        "username",
        "name",
        "email",
        "is_verified",
        "company_name",
        "is_superuser",
    )

    # Fields to search by
    search_fields = ("username", "name", "email")

    # Filters available in the sidebar
    list_filter = ("is_verified", "auth_method", "is_superuser")

    # Allows filtering by specific fields in the list view
    ordering = ("username",)


# Register the CustomUserAdmin with the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(FabricColorImage)
class FabricColorImageAdmin(admin.ModelAdmin):
    list_display = ("fabric", "color")
    search_fields = ("fabric__title", "color")


class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_number",
        "user",
        "request_type",
        "current_status_or_order_status",
        "created_at",
    )

    list_filter = ("request_type", "current_status", "order_status")

    search_fields = (
        "request_number",  # For searching by request_number
        "user__username",  # For searching by username (assuming user is a ForeignKey to a User model with a 'username' field)
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Override get_form to customize the fields based on request_type.
        """
        form = super(ContactRequestAdmin, self).get_form(request, obj, **kwargs)
        if obj:  # When editing an existing object
            if obj.request_type == "general":
                # Hide related_order and related_fabric
                form.base_fields["related_order"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
                form.base_fields["related_fabric"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
            elif obj.request_type == "product":
                # Hide related_order
                form.base_fields["related_order"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
                # Show related_fabric
                form.base_fields["related_fabric"].required = True
            elif obj.request_type == "product_request":
                # Hide related_fabric
                form.base_fields["related_fabric"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
                # Show related_order
                form.base_fields["related_order"].required = True
        else:  # When creating a new object
            request_type = request.GET.get("request_type")
            if request_type == "general":
                # Hide related_order and related_fabric
                form.base_fields["related_order"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
                form.base_fields["related_fabric"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
            elif request_type == "product":
                # Hide related_order
                form.base_fields["related_order"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
                # Show related_fabric
                form.base_fields["related_fabric"].required = True
            elif request_type == "product_request":
                # Hide related_fabric
                form.base_fields["related_fabric"].widget = (
                    admin.widgets.AdminTextInputWidget(attrs={"type": "hidden"})
                )
                # Show related_order
                form.base_fields["related_order"].required = True
        return form

    def current_status_or_order_status(self, obj):
        """
        Display the correct status field based on the request_type.
        """
        if obj.request_type == "product_request":
            return obj.order_status
        return obj.current_status

    current_status_or_order_status.short_description = "Status"

    def save_model(self, request, obj, form, change):
        if change:  # If the object is being updated
            old_obj = ContactRequest.objects.get(pk=obj.pk)
            if old_obj.current_status != obj.current_status:
                self.send_status_update_email(obj, "current_status")
            if old_obj.order_status != obj.order_status:
                self.send_status_update_email(obj, "order_status")

        super(ContactRequestAdmin, self).save_model(request, obj, form, change)

    def send_status_update_email(self, obj, status_type):
        subject = f"Your {status_type.replace('_', ' ')} has been updated"
        message = f"Dear {obj.user.name},\n\nYour request's {status_type.replace('_', ' ')} has been updated to '{getattr(obj, status_type)}'.\n\nThank you!"
        from_email = settings.DEFAULT_FROM_EMAIL

        recipient_list = [obj.user.email]

        send_mail(subject, message, from_email, recipient_list)


admin.site.register(ContactRequest, ContactRequestAdmin)
