import django_filters
from django_filters import rest_framework as filters
from .models import Blog


class BlogFilter(filters.FilterSet):
    tags = django_filters.CharFilter(method="filter_by_tags")

    class Meta:
        model = Blog
        fields = ["tags"]

    def filter_by_tags(self, queryset, name, value):
        tags = value.split(",")
        return queryset.filter(tags__in=tags).distinct()
