import django_filters
from django_filters import rest_framework as filters
from .models import Fabric, ProductCategory, Blog
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
    sort_by = filters.OrderingFilter(
        fields=(
            ("created_at", "newest"),
            ("-created_at", "oldest"),
            ("num_orders", "most_requested"),
        ),
        field_labels={
            "newest": "Newest",
            "oldest": "Oldest",
            "most_requested": "Most Requested",
        },
        label="sort by",
    )
    colors = filters.BaseInFilter(field_name="available_colors", lookup_expr="contains")
    item_code = filters.CharFilter(field_name="item_code", lookup_expr="icontains")

    class Meta:
        model = Fabric
        fields = ["keyword", "sort_by", "colors", "item_code"]

    def filter_by_keyword(self, queryset, name, value):
        value = value.lower()
        if "best_selling" in value:
            queryset = Fabric.objects.annotate(
                num_orders=Count("orderitem_set")
            ).order_by("-num_orders")
        elif "hot_selling" in value:
            queryset = queryset.filter(is_hot_selling=True)
        else:
            category = ProductCategory.objects.filter(name__icontains=value).first()
            if category:
                queryset = queryset.filter(product_category=category)
            else:
                queryset = queryset.filter(
                    Q(title__icontains=value) | Q(item_code__icontains=value)
                )
        return queryset

    def filter_queryset(self, queryset):
        # Annotate the queryset with the number of orders
        queryset = queryset.annotate(num_orders=Count("orderitem_set"))
        # Apply the usual filter logic
        return super().filter_queryset(queryset)
