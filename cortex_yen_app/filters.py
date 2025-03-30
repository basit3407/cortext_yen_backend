import django_filters
from django_filters import rest_framework as filters
from .models import Fabric, ProductCategory, Blog, FabricColorCategory
from django.db.models import Count, Q


class BlogFilter(filters.FilterSet):
    category = django_filters.CharFilter(method="filter_by_category")

    class Meta:
        model = Blog
        fields = ["category"]

    def filter_by_category(self, queryset, name, value):
        categories = value.split(",")
        return queryset.filter(category__name__in=categories).distinct()


class FabricFilter(filters.FilterSet):
    keyword = filters.CharFilter(method="filter_by_keyword")
    sort_by = filters.CharFilter(method="apply_sorting")
    colors = filters.CharFilter(method="filter_by_colors")
    item_code = filters.CharFilter(field_name="item_code", lookup_expr="icontains")
    category = filters.NumberFilter(
        field_name="color_images__color_category__id", lookup_expr="exact"
    )

    class Meta:
        model = Fabric
        fields = ["keyword", "sort_by", "colors", "item_code", "category"]

    def filter_by_keyword(self, queryset, name, value):
        if not value:
            return queryset
            
        if value == "best_selling":
            return Fabric.objects.annotate(
                num_orders=Count('orderitem_set')
            ).order_by("-num_orders", "-is_hot_selling")
            
        # Check if the keyword matches a product category name
        try:
            category = ProductCategory.objects.get(name__iexact=value)
            return queryset.filter(product_category=category)
        except ProductCategory.DoesNotExist:
            # If not a product category, search in fabric fields
            return queryset.filter(
                Q(title__icontains=value) |
                Q(description__icontains=value) |
                Q(composition__icontains=value) |
                Q(item_code__icontains=value)
            )

    def filter_by_colors(self, queryset, name, value):
        if not value:
            return queryset
            
        # Split the comma-separated color IDs
        color_ids = [int(color_id.strip()) for color_id in value.split(',') if color_id.strip().isdigit()]
        
        if not color_ids:
            return queryset
            
        # Filter fabrics that have any of the specified colors
        return queryset.filter(
            color_images__color_category_id__in=color_ids
        ).distinct()
        
    def apply_sorting(self, queryset, name, value):
        if not value:
            # Default to newest if no sorting specified
            return queryset.order_by('-created_at')
            
        if value == 'newest':
            return queryset.order_by('-created_at')
        elif value == 'oldest':
            return queryset.order_by('created_at')
        elif value == 'most_requested':
            # Annotate with order count and sort
            return queryset.annotate(
                num_orders=Count('orderitem_set')
            ).order_by('-num_orders')
        
        # Default to newest if invalid sort option
        return queryset.order_by('-created_at')
