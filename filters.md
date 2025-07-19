# API Filtering Documentation

This document outlines the filtering capabilities available for the Corlee & Co backend API endpoints. All filtering is implemented using Django REST Framework's filtering backend and supports partial text matching.

## Overview

The API supports filtering for three main endpoints:
- **Fabrics** (`/api/fabrics/`)
- **Blogs** (`/api/blogs/`)
- **Users** (`/api/users/`)

All filters use **partial matching** (case-insensitive), meaning any text you search for will match if it appears anywhere within the field.

## Users Filtering

**Endpoint:** `/api/users/`

### Available Filter Parameters

| Parameter | Description | Type | Example |
|-----------|-------------|------|---------|
| `name` | Filter by user's name (partial match) | String | `?name=john` |
| `company_name` | Filter by company name (partial match) | String | `?company_name=textile` |
| `address` | Filter by user's address (partial match) | String | `?address=new york` |
| `phone` | Filter by phone number (partial match) | String | `?phone=123` |
| `mobile_phone` | Filter by mobile phone (partial match) | String | `?mobile_phone=456` |
| `email` | Filter by email address (partial match) | String | `?email=gmail` |

### Usage Examples

```
# Find users with "john" in their name
GET /api/users/?name=john

# Find users with "textile" in their company name
GET /api/users/?company_name=textile

# Find users with "gmail" in their email
GET /api/users/?email=gmail

# Multiple filters (AND operation)
GET /api/users/?name=john&email=gmail&phone=123

# Find users with "765" in phone and "uzairmanan" in email
GET /api/users/?email=uzairmanan&phone=765
```

## Fabrics Filtering

**Endpoint:** `/api/fabrics/`

### Available Filter Parameters

| Parameter | Description | Type | Example |
|-----------|-------------|------|---------|
| `keyword` | Search across title, description, composition, item_code, and category names (English & Mandarin) | String | `?keyword=cotton` |
| `sort_by` | Sort results | String | `?sort_by=newest` |
| `colors` | Filter by color category IDs (comma-separated) | String | `?colors=1,2,3` |
| `item_code` | Filter by item code (partial match) | String | `?item_code=FAB001` |
| `category` | Filter by specific color category ID | Integer | `?category=5` |
| `extra_categories` | Filter by product category IDs (comma-separated) | String | `?extra_categories=1,2` |

### Special Keywords

- `keyword=best_selling` - Returns only fabrics marked as hot selling

### Sort Options

- `newest` (default) - Sort by creation date, newest first
- `oldest` - Sort by creation date, oldest first
- `most_requested` - Sort by number of orders, most requested first

### Usage Examples

```
# Search for cotton fabrics
GET /api/fabrics/?keyword=cotton

# Get best selling fabrics sorted by newest
GET /api/fabrics/?keyword=best_selling&sort_by=newest

# Filter by specific colors
GET /api/fabrics/?colors=1,2,3

# Filter by item code
GET /api/fabrics/?item_code=FAB

# Multiple filters
GET /api/fabrics/?keyword=silk&colors=1&sort_by=most_requested
```

## Blogs Filtering

**Endpoint:** `/api/blogs/`

### Available Filter Parameters

| Parameter | Description | Type | Example |
|-----------|-------------|------|---------|
| `category` | Filter by blog category names (comma-separated, supports English & Mandarin) | String | `?category=news,fashion` |

### Usage Examples

```
# Filter by single category
GET /api/blogs/?category=news

# Filter by multiple categories
GET /api/blogs/?category=news,fashion

# Filter by Mandarin category names
GET /api/blogs/?category=时尚,新闻
```

## General Guidelines

### Multiple Filters
- All filters use **AND** logic when combined
- Example: `?name=john&email=gmail` returns users that have "john" in name AND "gmail" in email

### Pagination
All filtered results support pagination:
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10)

Example: `/api/users/?name=john&page=2&page_size=20`

### Case Sensitivity
All text filters are **case-insensitive**:
- `?name=JOHN` and `?name=john` return the same results

### URL Encoding
Remember to URL encode special characters:
- Spaces: `%20` or `+`
- Special characters should be properly encoded

### Response Format
All endpoints return the same pagination structure:
```json
{
    "count": 25,
    "next": "http://example.com/api/users/?page=2",
    "previous": null,
    "results": [...]
}
```

## Error Handling

### Invalid Parameters
- Invalid filter parameters are ignored
- The API will return results without applying invalid filters

### Empty Results
- If no results match the filters, an empty results array is returned
- The `count` field will be 0

### Examples of Invalid Usage
```
# Invalid color ID (non-numeric) - will be ignored
GET /api/fabrics/?colors=abc,def

# Invalid category ID - will be ignored  
GET /api/fabrics/?extra_categories=invalid
```

## Testing the Filters

### Frontend Implementation Tips

1. **Build Filter Forms**: Create form inputs for each filter parameter
2. **Construct Query Strings**: Combine multiple filters with `&`
3. **Handle Empty States**: Show appropriate messages when no results found
4. **Debounce Search**: Implement debouncing for real-time search to avoid excessive API calls
5. **URL State Management**: Consider updating the browser URL to reflect current filters

### Example Frontend URLs

```javascript
// Single filter
const url = `/api/users/?name=${encodeURIComponent(searchName)}`;

// Multiple filters
const filters = [];
if (name) filters.push(`name=${encodeURIComponent(name)}`);
if (email) filters.push(`email=${encodeURIComponent(email)}`);
if (phone) filters.push(`phone=${encodeURIComponent(phone)}`);

const url = `/api/users/?${filters.join('&')}`;
```

### Testing Examples

```bash
# Test user filtering
curl "http://localhost:8000/api/users/?name=john&email=gmail"

# Test fabric filtering  
curl "http://localhost:8000/api/fabrics/?keyword=cotton&sort_by=newest"

# Test blog filtering
curl "http://localhost:8000/api/blogs/?category=news,fashion"
```

## Implementation Details

The filtering is implemented using:
- **Django Filter**: `django-filter` package
- **DjangoFilterBackend**: REST framework filter backend
- **FilterSet Classes**: Custom filter classes for each model
- **Partial Matching**: Using `icontains` lookup for text fields

All filters follow the same patterns for consistency and maintainability.