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
    sort_by = filters.OrderingFilter(
        fields=(
            ("created_at", "oldest"),
            ("-created_at", "newest"),
            ("num_orders", "most_requested"),
        ),
        field_labels={
            "newest": "Newest",
            "oldest": "Oldest",
            "most_requested": "Most Requested",
        },
        label="sort by",
    )
    colors = filters.BaseInFilter(method="filter_by_colors")
    item_code = filters.CharFilter(field_name="item_code", lookup_expr="icontains")
    category = filters.NumberFilter(
        field_name="color_images__color_category__id", lookup_expr="exact"
    )

    class Meta:
        model = Fabric
        fields = ["keyword", "sort_by", "colors", "item_code", "category"]

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

    def filter_by_colors(self, queryset, name, value):
        color_ids = FabricColorCategory.objects.filter(id__in=value).values_list(
            "id", flat=True
        )
        queryset = queryset.filter(
            color_images__color_category__in=color_ids
        ).distinct()
        return queryset
