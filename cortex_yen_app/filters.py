import django_filters
from django_filters import rest_framework as filters
from .models import Fabric, ProductCategory, Blog, FabricColorCategory, BlogCategory
from django.db.models import Count, Q
import logging

logger = logging.getLogger(__name__)


class BlogFilter(filters.FilterSet):
    category = django_filters.CharFilter(method="filter_by_category")

    class Meta:
        model = Blog
        fields = ["category"]

    def filter_by_category(self, queryset, name, value):
        if not value:
            return queryset
        
        logger.info(f"BlogFilter filtering by category: '{value}'")
        categories = value.split(",")
        logger.info(f"Searching for categories: {categories}")
        
        # First try to find categories matching the English names
        english_matches = list(BlogCategory.objects.filter(name__in=categories).values_list('name', flat=True))
        if english_matches:
            logger.info(f"Found matching English category names: {english_matches}")
            
        # Then try to find categories matching the Mandarin names
        mandarin_matches = list(BlogCategory.objects.filter(name_mandarin__in=categories).values_list('name_mandarin', flat=True))
        if mandarin_matches:
            logger.info(f"Found matching Mandarin category names: {mandarin_matches}")
            
        # Filter by both English and Mandarin category names
        result = queryset.filter(
            Q(category__name__in=categories) | 
            Q(category__name_mandarin__in=categories)
        ).distinct()
        
        logger.info(f"Query returned {result.count()} results")
        return result


class FabricFilter(filters.FilterSet):
    keyword = filters.CharFilter(method="filter_by_keyword")
    sort_by = filters.CharFilter(method="apply_sorting")
    colors = filters.CharFilter(method="filter_by_colors")
    item_code = filters.CharFilter(field_name="item_code", lookup_expr="icontains")
    category = filters.NumberFilter(
        field_name="color_images__color_category__id", lookup_expr="exact"
    )
    extra_categories = filters.CharFilter(method="filter_by_extra_categories")

    class Meta:
        model = Fabric
        fields = ["keyword", "sort_by", "colors", "item_code", "category", "extra_categories"]

    def filter_by_keyword(self, queryset, name, value):
        if not value:
            return queryset
            
        logger.info(f"FabricFilter filtering by keyword: '{value}'")
            
        if value == "best_selling":
            # Return only fabrics marked as hot selling
            logger.info("Filtering for best selling fabrics")
            queryset = queryset.filter(is_hot_selling=True)
            
            # Let the sort_by parameter handle sorting (will be applied later)
            return queryset
            
        # Check if the keyword matches a product category name or mandarin name
        try:
            # Check for exact match in English name
            english_category = ProductCategory.objects.filter(name__iexact=value).first()
            if english_category:
                logger.info(f"Found matching English category name: {english_category.name}")
                return queryset.filter(
                    Q(product_category=english_category) |
                    Q(extra_categories=english_category)
                ).distinct()
                
            # Check for exact match in Mandarin name
            mandarin_category = ProductCategory.objects.filter(name_mandarin__iexact=value).first()
            if mandarin_category:
                logger.info(f"Found matching Mandarin category name: {mandarin_category.name_mandarin} (English: {mandarin_category.name})")
                return queryset.filter(
                    Q(product_category=mandarin_category) |
                    Q(extra_categories=mandarin_category)
                ).distinct()
            
            # If no exact match found, search in other fabric fields
            logger.info(f"No matching category found for '{value}', searching in fabric fields")
            return queryset.filter(
                Q(title__icontains=value) |
                Q(title_mandarin__icontains=value) |
                Q(description__icontains=value) |
                Q(description_mandarin__icontains=value) |
                Q(composition__icontains=value) |
                Q(composition_mandarin__icontains=value) |
                Q(item_code__icontains=value)
            )
        except Exception as e:
            logger.error(f"Error in filter_by_keyword: {str(e)}")
            # Fallback to basic filtering if any error occurs
            return queryset.filter(
                Q(title__icontains=value) |
                Q(title_mandarin__icontains=value) |
                Q(description__icontains=value) |
                Q(description_mandarin__icontains=value) |
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
        # Log the sorting parameter for debugging
        logger.info(f"Applying sorting with value: '{value}'")
        
        if not value or value.lower() == 'newest':
            # Default to newest if no sorting specified or if 'newest' is explicitly requested
            return queryset.order_by('-created_at')
            
        elif value.lower() == 'oldest':
            return queryset.order_by('created_at')
            
        elif value.lower() == 'most_requested':
            # Annotate with order count and sort
            return queryset.annotate(
                num_orders=Count('orderitem_set')
            ).order_by('-num_orders')
        
        # Default to newest for any unrecognized sort option
        logger.warning(f"Unrecognized sort_by value: '{value}', defaulting to newest")
        return queryset.order_by('-created_at')

    def filter_by_extra_categories(self, queryset, name, value):
        if not value:
            return queryset
            
        # Split the comma-separated category IDs
        category_ids = [int(cat_id.strip()) for cat_id in value.split(',') if cat_id.strip().isdigit()]
        
        if not category_ids:
            return queryset
            
        # Filter fabrics that have any of the specified extra categories
        return queryset.filter(
            Q(product_category_id__in=category_ids) |
            Q(extra_categories__id__in=category_ids)
        ).distinct()
