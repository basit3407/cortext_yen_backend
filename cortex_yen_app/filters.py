import django_filters
from django_filters import rest_framework as filters
from .models import Blog


class BlogFilter(filters.FilterSet):
    category = django_filters.CharFilter(method="filter_by_category")

    class Meta:
        model = Blog
        fields = ["category"]

    def filter_by_category(self, queryset, name, value):
        categories = value.split(",")
        return queryset.filter(category__in=categories).distinct()
